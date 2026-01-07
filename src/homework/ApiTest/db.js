import mysql from 'mysql2/promise';

export const db = await mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '1234',
  port: 3306,
  database: 'elice', // 실제 DB명으로 바꿔
  waitForConnections: true,
  connectionLimit: 10,
});
