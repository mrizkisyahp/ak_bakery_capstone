const errorHandler = (err, req, res, next) => {
  let statusCode = err.statusCode || 500;
  let status = err.status || 'error';
  let message = err.message || 'Terjadi kesalahan internal pada server';

  // Tangani error validasi Joi
  if (err.isJoi) {
    statusCode = 400;
    status = 'fail';
    message = err.details ? err.details.map((d) => d.message).join(', ') : err.message;
  }

  const response = {
    status,
    message
  };

  if (process.env.NODE_ENV === 'development') {
    response.stack = err.stack;
  }

  return res.status(statusCode).json(response);
};

module.exports = errorHandler;

