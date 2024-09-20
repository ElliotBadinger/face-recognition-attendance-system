const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const rateLimit = require("express-rate-limit");
const helmet = require("helmet");

const app = express();
const port = 3000;

// Add security headers
app.use(helmet());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Proxy middleware options
const options = {
  target: 'http://localhost', // target host
  changeOrigin: true, // needed for virtual hosted sites
  ws: true, // proxy websockets
};

// Create the proxy middleware
const faceRecognitionProxy = createProxyMiddleware(options);
const userManagementProxy = createProxyMiddleware(options);
const authenticationProxy = createProxyMiddleware(options);
const attendanceProxy = createProxyMiddleware(options);
const notificationProxy = createProxyMiddleware(options);
const analyticsProxy = createProxyMiddleware(options);

// Proxy routes
app.use('/face-recognition', faceRecognitionProxy);
app.use('/user-management', userManagementProxy);
app.use('/auth', authenticationProxy);
app.use('/attendance', attendanceProxy);
app.use('/notification', notificationProxy);
app.use('/analytics', analyticsProxy);

// Start the Gateway
app.listen(port, () => {
  console.log(`API Gateway listening at http://localhost:${port}`);
});