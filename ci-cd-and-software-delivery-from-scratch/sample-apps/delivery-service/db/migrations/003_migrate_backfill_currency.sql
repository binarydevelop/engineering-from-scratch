-- Migration 003: Migrate Phase (Data Backfill & Transformation)
-- Backfill historical rows that might have NULL or unnormalized values.
UPDATE orders SET currency = 'USD' WHERE currency IS NULL OR currency = '';
