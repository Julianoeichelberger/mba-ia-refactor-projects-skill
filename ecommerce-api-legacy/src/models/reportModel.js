const { dbAll } = require('./database');

async function getFinancialReport() {
    const rows = await dbAll(`
        SELECT
            c.id AS course_id,
            c.title AS course_title,
            u.name AS student_name,
            p.amount,
            p.status
        FROM courses c
        LEFT JOIN enrollments e ON c.id = e.course_id
        LEFT JOIN users u ON e.user_id = u.id
        LEFT JOIN payments p ON e.id = p.enrollment_id
        ORDER BY c.id
    `);
    return rows;
}

module.exports = { getFinancialReport };
