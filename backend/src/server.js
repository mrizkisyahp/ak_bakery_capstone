const app = require('./app');

const PORT = process.env.PORT || 5000;

const server = app.listen(PORT, () => {
  console.log(`🚀 Backend AK Bakery is running on http://localhost:${PORT}`);
  console.log(`🩺 Health check ready at http://localhost:${PORT}/api/v1/health`);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  console.error('💥 UNHANDLED REJECTION! Shutting down...');
  console.error(err.name, err.message);
  server.close(() => {
    process.exit(1);
  });
});

