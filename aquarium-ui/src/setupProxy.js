const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Proxy for aquarium-manager-service
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',
      changeOrigin: true,
      logLevel: 'debug',
      onProxyReq: (proxyReq, req, res) => {
        console.log('Aquarium Manager - Proxying request:', req.method, req.url, '-> http://localhost:5000' + proxyReq.path);
      },
      onProxyRes: (proxyRes, req, res) => {
        console.log('Aquarium Manager - Received response:', proxyRes.statusCode, req.url);
      },
      onError: (err, req, res) => {
        console.error('Aquarium Manager - Proxy error:', err);
        res.status(500).json({ error: 'Aquarium Manager Proxy error', details: err.message });
      }
    })
  );

  // Proxy for fish-service
  app.use(
    '/fish_status',
    createProxyMiddleware({
      target: 'http://localhost:5001',
      changeOrigin: true,
      logLevel: 'debug',
      onProxyReq: (proxyReq, req, res) => {
        console.log('Fish Service - Proxying request:', req.method, req.url, '-> http://localhost:5001' + proxyReq.path);
      },
      onProxyRes: (proxyRes, req, res) => {
        console.log('Fish Service - Received response:', proxyRes.statusCode, req.url);
      },
      onError: (err, req, res) => {
        console.error('Fish Service - Proxy error:', err);
        res.status(500).json({ error: 'Fish Service Proxy error', details: err.message });
      }
    })
  );

  // Global error handler
  app.use((err, req, res, next) => {
    console.error('Global error:', err);
    res.status(500).json({ error: 'Internal server error', details: err.message });
  });
};