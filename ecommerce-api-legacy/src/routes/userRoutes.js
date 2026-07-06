const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

router.delete('/api/users/:id', async (req, res, next) => {
    try {
        const result = await userController.deleteUser(req.params.id);
        res.json(result);
    } catch (error) {
        next(error);
    }
});

module.exports = router;
