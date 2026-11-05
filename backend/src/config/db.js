const { Pool } = require('pg');
require('dotenv').config();

const connectionString = process.env.DATABASE_URL;

const pool = new Pool({
  connectionString,
  ssl: connectionString && connectionString.includes('neon.tech') ? { rejectUnauthorized: false } : false
});

pool.on('connect', () => {
  console.log(' Connected to PostgreSQL Database');
});

pool.on('error', (err) => {
  console.error(' Unexpected error on idle PostgreSQL client:', err);
});

module.exports = {
  query: (text, params) => pool.query(text, params),
  pool
};

