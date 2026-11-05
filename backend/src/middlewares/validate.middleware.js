const validate = (schema) => (req, res, next) => {
  const { error, value } = schema.validate(req.body, {
    abortEarly: false,
    stripUnknown: true
  });

  if (error) {
    error.isJoi = true;
    return next(error);
  }

  // Assign validated and sanitized values back to req.body
  req.body = value;
  next();
};

module.exports = validate;

