const express = require('express');
const cors = require('cors');
require('dotenv').config();

const apiRoutes = require('./routes');
const errorHandler = require('./middlewares/error.middleware');
const AppError = require('./utils/appError');

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Base Route
app.get('/', (req, res) => {
  res.status(200).json({
    status: 'success',
    message: 'Welcome to Adiskirani Bakery (AK) API. Use /api/v1/health to check service status.'
  });
});

// API v1 Routes
app.use('/api/v1', apiRoutes);

// Catch-all middleware for undefined endpoints (Express 5 compatible)
app.use((req, res, next) => {
  next(new AppError(`Endpoint ${req.originalUrl} tidak ditemukan pada server ini.`, 404));
});

// Centralized Error Handler
app.use(errorHandler);

module.exports = app;
