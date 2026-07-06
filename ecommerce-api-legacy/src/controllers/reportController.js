const reportModel = require('../models/reportModel');

async function getFinancialReport() {
    const rows = await reportModel.getFinancialReport();

    const coursesMap = new Map();

    for (const row of rows) {
        if (!coursesMap.has(row.course_id)) {
            coursesMap.set(row.course_id, {
                course: row.course_title,
                revenue: 0,
                students: [],
            });
        }

        const courseData = coursesMap.get(row.course_id);

        if (row.student_name) {
            if (row.status === 'PAID') {
                courseData.revenue += row.amount;
            }
            courseData.students.push({
                student: row.student_name,
                paid: row.amount || 0,
            });
        }
    }

    return Array.from(coursesMap.values());
}

module.exports = { getFinancialReport };
