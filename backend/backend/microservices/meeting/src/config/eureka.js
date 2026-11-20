const { Eureka } = require('eureka-js-client');

/**
 * Builds the Eureka client that registers this microservice as "MEETING".
 * The port is passed in so several instances (different PORT values) can run side by side.
 */
function createEurekaClient(port) {
  const host = process.env.EUREKA_HOST || 'localhost';
  const eurekaPort = Number(process.env.EUREKA_PORT || 8761);
  const hostName = process.env.HOSTNAME_EUREKA || 'localhost';

  return new Eureka({
    instance: {
      app: 'MEETING',
      instanceId: `${hostName}:meeting:${port}`,
      hostName,
      ipAddr: '127.0.0.1',
      statusPageUrl: `http://${hostName}:${port}/info`,
      healthCheckUrl: `http://${hostName}:${port}/health`,
      homePageUrl: `http://${hostName}:${port}/`,
      port: { $: Number(port), '@enabled': true },
      vipAddress: 'meeting',
      dataCenterInfo: {
        '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
        name: 'MyOwn',
      },
    },
    eureka: {
      host,
      port: eurekaPort,
      servicePath: '/eureka/apps/',
      maxRetries: 10,
      requestRetryDelay: 2000,
    },
  });
}

module.exports = createEurekaClient;
