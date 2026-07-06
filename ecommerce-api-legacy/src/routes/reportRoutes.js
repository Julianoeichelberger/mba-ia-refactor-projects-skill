const express = require('express');
const router = express.Router();
const reportController = require('../controllers/reportController');

router.get('/api/admin/financial-report', async (req, res, next) => {
    try {
        const report = await reportController.getFinancialReport();
        res.json(report);
    } catch (error) {
        next(error);
    }
});

module.exports = router;
