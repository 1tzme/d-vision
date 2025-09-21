-- Helpers (functions) for checking some data types (for safe data parsing)

-- function for int
CREATE OR REPLACE FUNCTION raw.safe_int(txt TEXT) RETURNS INTEGER AS $$
BEGIN
  IF txt IS NULL OR trim(txt) = '' THEN RETURN NULL; END IF;
  IF txt ~ '^-?\d+$' THEN RETURN txt::int; ELSE RETURN NULL; END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- function for numeric
CREATE OR REPLACE FUNCTION raw.safe_numeric(txt TEXT) RETURNS NUMERIC AS $$
DECLARE v NUMERIC;
BEGIN
  IF txt IS NULL OR trim(txt) = '' THEN RETURN NULL; END IF;
  txt := regexp_replace(txt, '[^0-9\.\-]', '', 'g');
  IF txt = '' THEN RETURN NULL; END IF;
  v := txt::numeric;
  RETURN v;
EXCEPTION WHEN others THEN RETURN NULL;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- function for date
CREATE OR REPLACE FUNCTION raw.safe_date(txt TEXT) RETURNS DATE AS $$
DECLARE d DATE;
BEGIN
  IF txt IS NULL OR trim(txt) = '' THEN RETURN NULL; END IF;
  -- ISO yyyy-mm-dd
  BEGIN d := txt::date; RETURN d; EXCEPTION WHEN others THEN NULL; END;
  -- dd/mm/yyyy
  BEGIN d := to_date(txt,'DD/MM/YYYY'); RETURN d; EXCEPTION WHEN others THEN NULL; END;
  -- dd-mm-yyyy
  BEGIN d := to_date(txt,'DD-MM-YYYY'); RETURN d; EXCEPTION WHEN others THEN NULL; END;
  -- mm/dd/yyyy
  BEGIN d := to_date(txt,'MM/DD/YYYY'); RETURN d; EXCEPTION WHEN others THEN NULL; END;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- function for timestamp
CREATE OR REPLACE FUNCTION raw.safe_timestamp(txt TEXT) RETURNS TIMESTAMP AS $$
DECLARE t TIMESTAMP;
BEGIN
  IF txt IS NULL OR trim(txt) = '' THEN RETURN NULL; END IF;
  BEGIN t := txt::timestamp; RETURN t; EXCEPTION WHEN others THEN NULL; END;
  BEGIN t := to_timestamp(txt,'DD/MM/YYYY HH24:MI:SS'); RETURN t; EXCEPTION WHEN others THEN NULL; END;
  BEGIN t := to_timestamp(txt,'YYYY-MM-DD"T"HH24:MI:SS'); RETURN t; EXCEPTION WHEN others THEN NULL; END;
  BEGIN t := to_timestamp(txt,'YYYY-MM-DD HH24:MI:SS'); RETURN t; EXCEPTION WHEN others THEN NULL; END;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
