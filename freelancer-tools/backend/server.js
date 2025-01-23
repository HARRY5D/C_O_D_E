// backend/server.js
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const connectDB = require('./config/db');

const app = express();

// Connect to Database
connectDB();

// Middleware
app.use(cors());
app.use(helmet());
app.use(express.json());

// Routes
app.use('/api/tools', require('./routes/toolRoutes'));
app.use('/api/users', require('./routes/userRoutes'));
app.use('/api/admin', require('./routes/adminRoutes'));

// Add this to your server.js temporarily
app.get('/test', (req, res) => {
    res.json({
        mongodb: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
        redis: client.isReady ? 'connected' : 'disconnected'
    });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));