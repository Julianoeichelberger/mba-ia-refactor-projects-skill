const sqlite3 = require('sqlite3').verbose();
const { dbPath } = require('../config/settings');

let db;

function getDb() {
    if (!db) {
        db = new sqlite3.Database(dbPath);
    }
    return db;
}

function dbRun(sql, params = []) {
    return new Promise((resolve, reject) => {
        getDb().run(sql, params, function (err) {
            err ? reject(err) : resolve({ lastID: this.lastID, changes: this.changes });
        });
    });
}

function dbGet(sql, params = []) {
    return new Promise((resolve, reject) => {
        getDb().get(sql, params, (err, row) => (err ? reject(err) : resolve(row)));
    });
}

function dbAll(sql, params = []) {
    return new Promise((resolve, reject) => {
        getDb().all(sql, params, (err, rows) => (err ? reject(err) : resolve(rows)));
    });
}

async function initDb() {
    await dbRun(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        pass TEXT NOT NULL
    )`);

    await dbRun(`CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        price REAL NOT NULL CHECK(price >= 0),
        active INTEGER NOT NULL DEFAULT 1
    )`);

    await dbRun(`CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
    )`);

    await dbRun(`CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY,
        enrollment_id INTEGER NOT NULL,
        amount REAL NOT NULL CHECK(amount >= 0),
        status TEXT NOT NULL,
        FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE
    )`);

    await dbRun(`CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY,
        action TEXT NOT NULL,
        created_at DATETIME NOT NULL
    )`);

    await dbRun("PRAGMA foreign_keys = ON");

    await seedDb();
}

async function seedDb() {
    const bcrypt = require('bcrypt');
    const existingUser = await dbGet("SELECT id FROM users WHERE email = ?", ['leonan@fullcycle.com.br']);
    if (existingUser) return;

    const hashedPass = await bcrypt.hash('123', 10);
    await dbRun("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", ['Leonan', 'leonan@fullcycle.com.br', hashedPass]);
    await dbRun("INSERT INTO courses (title, price, active) VALUES (?, ?, ?)", ['Clean Architecture', 997.00, 1]);
    await dbRun("INSERT INTO courses (title, price, active) VALUES (?, ?, ?)", ['Docker', 497.00, 1]);
    await dbRun("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [1, 1]);
    await dbRun("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [1, 997.00, 'PAID']);
}

module.exports = { getDb, dbRun, dbGet, dbAll, initDb };
