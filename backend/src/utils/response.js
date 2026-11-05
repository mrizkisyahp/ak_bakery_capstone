const successResponse = (res, statusCode, message, data = null) => {
  return res.status(statusCode).json({
    status: 'success',
    message,
    data
  });
};

const errorResponse = (res, statusCode, message) => {
  return res.status(statusCode).json({
    status: `${statusCode}`.startsWith('4') ? 'fail' : 'error',
    message
  });
};

module.exports = { successResponse, errorResponse };

