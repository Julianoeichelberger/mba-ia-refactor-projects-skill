const { dbRun } = require('./database');

async function create(enrollmentId, amount, status) {
    const result = await dbRun(
        "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
        [enrollmentId, amount, status]
    );
    return { id: result.lastID, enrollmentId, amount, status };
}

module.exports = { create };
