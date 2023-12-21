CREATE SCHEMA IF NOT EXISTS app;

SET search_path TO app;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE http_checks (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    uri VARCHAR NOT NULL,
    is_paused BOOLEAN NOT NULL,
    num_retries INTEGER NOT NULL CHECK (num_retries >= 1 AND num_retries <= 5),
    uptime_sla NUMERIC NOT NULL CHECK (uptime_sla >= 0 AND uptime_sla <= 100),
    response_time_sla NUMERIC NOT NULL CHECK (response_time_sla >= 0 AND response_time_sla <= 100),
    use_ssl BOOLEAN NOT NULL,
    response_status_code INTEGER NOT NULL DEFAULT 200,
    check_interval_in_seconds INTEGER NOT NULL CHECK (check_interval_in_seconds >= 1 AND check_interval_in_seconds <= 86400),
    check_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    check_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create a trigger to update check_updated on row updates
CREATE OR REPLACE FUNCTION update_check_updated()
RETURNS TRIGGER AS $$
BEGIN
  NEW.check_updated = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger that calls the update_check_updated function
CREATE TRIGGER update_check_updated_trigger
BEFORE UPDATE ON http_checks
FOR EACH ROW
EXECUTE FUNCTION update_check_updated();
