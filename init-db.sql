-- Initialize the database with any required extensions or initial data

-- Enable UUID extension (if needed)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create initial fraud patterns (these will be created by migrations, but kept as backup)
-- INSERT INTO fraud_patterns (pattern_name, pattern_type, description, parameters, threshold_score, is_active) VALUES
-- ('High Amount Transfer', 'amount', 'Transfers exceeding daily limits', '{"max_amount": 10000}', 0.7, true),
-- ('Velocity Check', 'velocity', 'Multiple transfers in short time', '{"max_hourly": 10, "max_daily": 50}', 0.6, true),
-- ('Geographic Anomaly', 'geographic', 'Transfers from unusual locations', '{"allowed_countries": ["US", "CA", "MX"]}', 0.5, true),
-- ('New Account Risk', 'account_age', 'Transfers from recently created accounts', '{"min_age_days": 7}', 0.4, true),
-- ('Round Number Pattern', 'behavioral', 'Preference for round numbers in fraud', '{"round_amount_threshold": 1000}', 0.3, true)
-- ON CONFLICT DO NOTHING;

-- Create indexes for performance (will be created by migrations)
-- These are kept here for reference

-- Transfers table indexes
-- CREATE INDEX IF NOT EXISTS idx_transfers_sender_id ON transfers(sender_id);
-- CREATE INDEX IF NOT EXISTS idx_transfers_receiver_id ON transfers(receiver_id);
-- CREATE INDEX IF NOT EXISTS idx_transfers_created_at ON transfers(created_at);
-- CREATE INDEX IF NOT EXISTS idx_transfers_status ON transfers(status);
-- CREATE INDEX IF NOT EXISTS idx_transfers_fraud_score ON transfers(fraud_score);

-- Fraud reports table indexes
-- CREATE INDEX IF NOT EXISTS idx_fraud_reports_user_id ON fraud_reports(user_id);
-- CREATE INDEX IF NOT EXISTS idx_fraud_reports_transfer_id ON fraud_reports(transfer_id);
-- CREATE INDEX IF NOT EXISTS idx_fraud_reports_created_at ON fraud_reports(created_at);

-- User behaviors table indexes
-- CREATE INDEX IF NOT EXISTS idx_user_behaviors_user_id ON user_behaviors(user_id);
-- CREATE INDEX IF NOT EXISTS idx_user_behaviors_created_at ON user_behaviors(created_at);

-- Sample data for testing (optional)
-- Uncomment the following lines if you want sample data during development

/*
-- Create sample users (passwords are hashed with bcrypt)
INSERT INTO users (email, username, hashed_password, full_name, balance, is_active, is_verified) VALUES
('alice@example.com', 'alice', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewowrXNvJJgDCsqy', 'Alice Johnson', 5000.00, true, true),
('bob@example.com', 'bob', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewowrXNvJJgDCsqy', 'Bob Smith', 3000.00, true, true),
('charlie@example.com', 'charlie', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewowrXNvJJgDCsqy', 'Charlie Brown', 2000.00, true, false)
ON CONFLICT (email) DO NOTHING;
*/

-- Performance optimization settings for PostgreSQL
SET shared_preload_libraries = 'pg_stat_statements';

-- Log slow queries (anything over 1 second)
SET log_min_duration_statement = 1000;

-- Enable query statistics
SET track_activities = on;
SET track_counts = on;
SET track_io_timing = on;
SET track_functions = 'all';

-- Optimize for our workload
SET random_page_cost = 1.1;  -- Assuming SSD storage
SET effective_cache_size = '256MB';  # Adjust based on available memory
SET maintenance_work_mem = '64MB';
SET checkpoint_completion_target = 0.9;
SET wal_buffers = '16MB';
SET default_statistics_target = 100;

-- Create a monitoring user (optional)
-- CREATE USER fraud_monitor WITH PASSWORD 'monitor_password';
-- GRANT CONNECT ON DATABASE fraud_detection TO fraud_monitor;
-- GRANT USAGE ON SCHEMA public TO fraud_monitor;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO fraud_monitor;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO fraud_monitor;

COMMIT;