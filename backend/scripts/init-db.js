const { pool } = require('../src/config/db');

const initDatabase = async () => {
  const client = await pool.connect();
  try {
    console.log('🔄 Memulai inisialisasi tabel di PostgreSQL...');

    await client.query('BEGIN');

    // 1. Tabel users
    await client.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL CHECK (role IN ('SUPERADMIN', 'ADMIN', 'SPG')),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 2. Tabel products (katalog bakery & snack box)
    await client.query(`
      CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(150) NOT NULL,
        category VARCHAR(50) NOT NULL,
        description TEXT,
        price_consumer NUMERIC(12, 2) NOT NULL,
        price_transmart NUMERIC(12, 2) NOT NULL,
        hpp NUMERIC(12, 2) NOT NULL,
        image_url TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 3. Tabel events (bazar / event pemerintah / instansi)
    await client.query(`
      CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        name VARCHAR(150) NOT NULL,
        location VARCHAR(200) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        status VARCHAR(20) DEFAULT 'UPCOMING' CHECK (status IN ('UPCOMING', 'ONGOING', 'COMPLETED')),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 4. Tabel transactions (arus kas masuk & keluar)
    await client.query(`
      CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id) ON DELETE SET NULL,
        event_id INT REFERENCES events(id) ON DELETE SET NULL,
        type VARCHAR(20) NOT NULL CHECK (type IN ('INCOME', 'EXPENSE')),
        category VARCHAR(50) NOT NULL,
        total_amount NUMERIC(14, 2) NOT NULL,
        estimated_cogs NUMERIC(14, 2) DEFAULT 0,
        estimated_profit NUMERIC(14, 2) DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 5. Tabel transaction_items (rincian roti per transaksi penjualan)
    await client.query(`
      CREATE TABLE IF NOT EXISTS transaction_items (
        id SERIAL PRIMARY KEY,
        transaction_id INT REFERENCES transactions(id) ON DELETE CASCADE,
        product_id INT REFERENCES products(id) ON DELETE SET NULL,
        quantity INT NOT NULL,
        price_per_unit NUMERIC(12, 2) NOT NULL,
        subtotal NUMERIC(12, 2) NOT NULL
      );
    `);

    // 6. Tabel feedbacks (testimoni pengunjung)
    await client.query(`
      CREATE TABLE IF NOT EXISTS feedbacks (
        id SERIAL PRIMARY KEY,
        customer_name VARCHAR(100) NOT NULL,
        customer_contact VARCHAR(100),
        message TEXT NOT NULL,
        rating INT DEFAULT 5 CHECK (rating BETWEEN 1 AND 5),
        is_approved BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 7. Tabel ai_chat_histories (Wajib Rubrik: Riwayat Gen AI)
    await client.query(`
      CREATE TABLE IF NOT EXISTS ai_chat_histories (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(100) NOT NULL,
        sender VARCHAR(10) NOT NULL CHECK (sender IN ('USER', 'BOT')),
        message TEXT NOT NULL,
        intent VARCHAR(50),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // 8. Tabel audit_logs (Mencatat perubahan penting)
    await client.query(`
      CREATE TABLE IF NOT EXISTS audit_logs (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id) ON DELETE SET NULL,
        action VARCHAR(100) NOT NULL,
        details JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `);

    await client.query('COMMIT');
    console.log('✅ Inisialisasi 8 tabel database berhasil!');
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('❌ Gagal menginisialisasi database:', error);
  } finally {
    client.release();
    await pool.end();
  }
};

initDatabase();

