const { dbRun, dbGet } = require('./database');
const bcrypt = require('bcrypt');

const SALT_ROUNDS = 10;

async function findByEmail(email) {
    return dbGet("SELECT id, name, email FROM users WHERE email = ?", [email]);
}

async function findById(id) {
    return dbGet("SELECT id, name, email FROM users WHERE id = ?", [id]);
}

async function create(name, email, password) {
    const hashedPass = await bcrypt.hash(password, SALT_ROUNDS);
    const result = await dbRun(
        "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
        [name, email, hashedPass]
    );
    return { id: result.lastID, name, email };
}

async function deleteById(id) {
    const result = await dbRun("DELETE FROM users WHERE id = ?", [id]);
    return result.changes > 0;
}

module.exports = { findByEmail, findById, create, deleteById };
