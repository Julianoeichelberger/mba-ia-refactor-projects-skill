const express = require('express');
const { port } = require('./config/settings');
const { initDb } = require('./models/database');
const registerRoutes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');

const app = express();
app.use(express.json());

registerRoutes(app);
app.use(errorHandler);

initDb()
    .then(() => {
        app.listen(port, () => {
            console.log(`LMS API rodando na porta ${port}`);
        });
    })
    .catch((err) => {
        console.error('Failed to initialize database:', err);
        process.exit(1);
    });
