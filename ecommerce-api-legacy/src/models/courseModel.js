const { dbGet, dbAll } = require('./database');

async function findActiveById(id) {
    return dbGet("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
}

async function findAll() {
    return dbAll("SELECT * FROM courses");
}

module.exports = { findActiveById, findAll };
