const express = require('express');
const router = express.Router();
const checkoutController = require('../controllers/checkoutController');

router.post('/api/checkout', async (req, res, next) => {
    try {
        const result = await checkoutController.checkout({
            username: req.body.usr,
            email: req.body.eml,
            password: req.body.pwd,
            courseId: req.body.c_id,
            card: req.body.card,
        });
        res.status(200).json(result);
    } catch (error) {
        next(error);
    }
});

module.exports = router;
