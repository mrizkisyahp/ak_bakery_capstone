const express = require('express');
const router = express.Router();
const { successResponse } = require('../utils/response');

// Health Check Endpoint
router.get('/health', (req, res) => {
  return successResponse(res, 200, 'Backend AK Bakery API is running perfectly!', {
    service: 'ak_bakery_backend',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;

