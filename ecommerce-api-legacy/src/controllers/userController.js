const userModel = require('../models/userModel');

class AppError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
    }
}

async function deleteUser(id) {
    const deleted = await userModel.deleteById(id);
    if (!deleted) {
        throw new AppError('Usuário não encontrado', 404);
    }
    return { msg: 'Usuário deletado com sucesso' };
}

module.exports = { deleteUser };
