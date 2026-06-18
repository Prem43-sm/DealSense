import { Pool } from "pg";

let pool: Pool | undefined;

export function getPool() {
  if (!process.env.DATABASE_URL) {
    throw new Error("DATABASE_URL is required to connect to PostgreSQL.");
  }

  pool ??= new Pool({
    connectionString: process.env.DATABASE_URL,
    max: 10,
    idleTimeoutMillis: 30000
  });

  return pool;
}
