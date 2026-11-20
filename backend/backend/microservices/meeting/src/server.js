const app = require('./app');
const createEurekaClient = require('./config/eureka');

// Port read from the PORT environment variable so several instances can run (8083, 8093, ...)
const PORT = Number(process.env.PORT || 8083);

const server = app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  // ---- Eureka registration (service name: MEETING) ----
  const eurekaClient = createEurekaClient(PORT);
  eurekaClient.start((error) => {
    console.log(error ? `Eureka registration failed: ${error.message}` : 'Registered in Eureka as MEETING');
  });

  // Unregister from Eureka when the process stops
  const shutdown = () => {
    eurekaClient.stop(() => server.close(() => process.exit(0)));
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
});
