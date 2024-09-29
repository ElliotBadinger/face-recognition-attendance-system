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

const options = {
  changeOrigin: true, // needed for virtual hosted sites
  ws: true, // proxy websockets
};

// Create the proxy middleware
const createServiceProxy = (target) => createProxyMiddleware({...options, target});

const faceRecognitionProxy = createServiceProxy('http://face_recognition:8000');
const userManagementProxy = createServiceProxy('http://user_management:8000');
const authenticationProxy = createServiceProxy('http://authentication:8000');
const attendanceProxy = createServiceProxy('http://attendance:8000');
const notificationProxy = createServiceProxy('http://notification:8000');
const analyticsProxy = createServiceProxy('http://analytics:8000');

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