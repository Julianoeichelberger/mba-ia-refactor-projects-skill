const courseModel = require('../models/courseModel');
const userModel = require('../models/userModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');
const auditLogModel = require('../models/auditLogModel');

class AppError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
    }
}

async function checkout({ username, email, password, courseId, card }) {
    if (!username || !email || !courseId || !card) {
        throw new AppError('Missing required fields: usr, eml, c_id, card', 400);
    }

    const course = await courseModel.findActiveById(courseId);
    if (!course) {
        throw new AppError('Curso não encontrado', 404);
    }

    let user = await userModel.findByEmail(email);
    if (!user) {
        user = await userModel.create(username, email, password || '123456');
    }

    const status = card.startsWith('4') ? 'PAID' : 'DENIED';
    if (status === 'DENIED') {
        throw new AppError('Pagamento recusado', 400);
    }

    const enrollment = await enrollmentModel.create(user.id, courseId);
    await paymentModel.create(enrollment.id, course.price, status);
    await auditLogModel.create(`Checkout curso ${courseId} por ${user.id}`);

    return { msg: 'Sucesso', enrollment_id: enrollment.id };
}

module.exports = { checkout };
