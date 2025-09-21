### 1. Open `psql` and connect to db
```bash
psql -U postgres -d finance
```

### 2. Create schema for raw data with TEXT types for all columns. Run `raw_tables.sql`

### 3. Load CSV to staging (with \copy). Run `copy.sql`

### 4. Create clean tables with correct types. Run `tables.sql`

### 5. Create helpers for safe parsing. Run `helper_functions.sql`

### 6. Filling tables. Run `table_filling.sql`

### 7. Checking referential integrity and cleaning. Run `checkers.sql`

### 8. Adding Foreign keys and Indexes. Run `foreign_keys.sql` and `indexes.sql`