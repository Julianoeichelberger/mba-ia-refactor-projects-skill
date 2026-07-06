require('dotenv').config();

module.exports = {
    secretKey: process.env.SECRET_KEY || 'dev-key-change-in-production',
    dbPath: process.env.DB_PATH || ':memory:',
    port: parseInt(process.env.PORT || '3000', 10),
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    smtpUser: process.env.SMTP_USER,
};
