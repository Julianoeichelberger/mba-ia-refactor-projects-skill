function errorHandler(err, req, res, next) {
    const status = err.status || 500;
    const message = status === 500 ? 'Internal server error' : err.message;

    if (status === 500) {
        console.error(`[ERROR] ${err.stack || err.message}`);
    }

    res.status(status).json({ error: message });
}

module.exports = errorHandler;
