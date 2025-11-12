# pip install requests flask prometheus-client
import time
import requests
from threading import Thread
from flask import Flask, Response
from prometheus_client import Gauge, generate_latest, REGISTRY

# Настройки
SUBREDDIT = "technology"  # можно заменить на любой саб
POLL_INTERVAL = 3  # каждые 3 секунды

# Метрики Reddit
reddit_subscribers = Gauge('reddit_subscribers', 'Number of subreddit subscribers', ['subreddit'])
reddit_active_users = Gauge('reddit_active_users', 'Number of currently active users', ['subreddit'])
reddit_posts_last = Gauge('reddit_posts_last_fetch', 'Number of posts fetched last cycle', ['subreddit'])
reddit_avg_score = Gauge('reddit_avg_score', 'Average score (upvotes - downvotes) for fetched posts', ['subreddit'])
reddit_avg_comments = Gauge('reddit_avg_comments', 'Average number of comments per post', ['subreddit'])
reddit_total_upvotes = Gauge('reddit_total_upvotes', 'Total upvotes for fetched posts', ['subreddit'])
reddit_total_downvotes = Gauge('reddit_total_downvotes', 'Estimated downvotes (approximation)', ['subreddit'])
reddit_top_post_score = Gauge('reddit_top_post_score', 'Score of top post in current batch', ['subreddit'])
reddit_top_post_comments = Gauge('reddit_top_post_comments', 'Number of comments on top post', ['subreddit'])
reddit_post_title_length_avg = Gauge('reddit_post_title_length_avg', 'Average title length of posts', ['subreddit'])
reddit_post_title_length_max = Gauge('reddit_post_title_length_max', 'Max title length among posts', ['subreddit'])
reddit_exporter_up = Gauge('up', 'Exporter status: 1 = healthy, 0 = error')
reddit_exporter_last_scrape = Gauge('reddit_exporter_last_scrape_unix', 'Unix timestamp of last successful scrape')

app = Flask(__name__)

def fetch_reddit_data(subreddit):
    """Получает данные о сабреддите и его последних постах."""
    base = f"https://www.reddit.com/r/{subreddit}/"
    headers = {"User-Agent": "PrometheusRedditExporter/1.0"}
    info = requests.get(base + "about.json", headers=headers, timeout=5)
    posts = requests.get(base + "new.json?limit=50", headers=headers, timeout=5)
    info.raise_for_status()
    posts.raise_for_status()
    return info.json(), posts.json()

def scrape_loop():
    while True:
        try:
            info, posts = fetch_reddit_data(SUBREDDIT)
            data = info.get("data", {})
            posts_data = posts.get("data", {}).get("children", [])

            subreddit = data.get("display_name", SUBREDDIT)
            subs = data.get("subscribers", 0)
            active = data.get("active_user_count", 0)
            reddit_subscribers.labels(subreddit=subreddit).set(subs)
            reddit_active_users.labels(subreddit=subreddit).set(active)

            if posts_data:
                scores = [p["data"].get("score", 0) for p in posts_data]
                comments = [p["data"].get("num_comments", 0) for p in posts_data]
                titles = [p["data"].get("title", "") for p in posts_data]

                avg_score = sum(scores) / len(scores)
                avg_comments = sum(comments) / len(comments)
                total_upvotes = sum(scores)
                estimated_downvotes = total_upvotes * 0.15
                top_post = max(posts_data, key=lambda x: x["data"].get("score", 0))["data"]
                top_score = top_post.get("score", 0)
                top_comments = top_post.get("num_comments", 0)
                avg_title_len = sum(len(t) for t in titles) / len(titles)
                max_title_len = max(len(t) for t in titles)

                reddit_posts_last.labels(subreddit=subreddit).set(len(posts_data))
                reddit_avg_score.labels(subreddit=subreddit).set(avg_score)
                reddit_avg_comments.labels(subreddit=subreddit).set(avg_comments)
                reddit_total_upvotes.labels(subreddit=subreddit).set(total_upvotes)
                reddit_total_downvotes.labels(subreddit=subreddit).set(estimated_downvotes)
                reddit_top_post_score.labels(subreddit=subreddit).set(top_score)
                reddit_top_post_comments.labels(subreddit=subreddit).set(top_comments)
                reddit_post_title_length_avg.labels(subreddit=subreddit).set(avg_title_len)
                reddit_post_title_length_max.labels(subreddit=subreddit).set(max_title_len)

            reddit_exporter_up.set(1)
            reddit_exporter_last_scrape.set(int(time.time()))

            print(f"[OK] {time.strftime('%H:%M:%S')} r/{SUBREDDIT}: {len(posts_data)} posts, {subs} subs")
        except Exception as e:
            print(f"[ERROR] {time.strftime('%H:%M:%S')} {e}")
            reddit_exporter_up.set(0)
        time.sleep(POLL_INTERVAL)

@app.route('/metrics')
def metrics():
    """Эндпоинт для Prometheus."""
    return Response(generate_latest(REGISTRY), mimetype='text/plain; version=0.0.4; charset=utf-8')

if __name__ == '__main__':
    print(f"Starting Reddit exporter for r/{SUBREDDIT}, updates every {POLL_INTERVAL}s")
    t = Thread(target=scrape_loop, daemon=True)
    t.start()
    app.run(host='localhost', port=8000)
