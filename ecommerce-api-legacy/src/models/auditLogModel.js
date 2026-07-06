const { dbRun } = require('./database');

async function create(action) {
    return dbRun(
        "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
        [action]
    );
}

module.exports = { create };
