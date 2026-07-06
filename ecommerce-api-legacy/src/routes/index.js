const checkoutRoutes = require('./checkoutRoutes');
const reportRoutes = require('./reportRoutes');
const userRoutes = require('./userRoutes');

function registerRoutes(app) {
    app.use(checkoutRoutes);
    app.use(reportRoutes);
    app.use(userRoutes);
}

module.exports = registerRoutes;
