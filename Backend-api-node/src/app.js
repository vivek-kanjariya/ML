const express = require('express');
const morgan = require('morgan');
const helmet = require('helmet');
const cors = require('cors');
const dotenv = require('dotenv');
const logger = require('./utils/logger');

dotenv.config();

const app = express();
app.use(express.json());
app.use(morgan('combined', { stream: logger.stream }));
app.use(helmet());
app.use(cors());

// Import routes
const predictRoutes = require('./routes/predict');
app.use('/api/predict', predictRoutes);

// Health check
app.get('/healthz', (req, res) => res.send('ok'));

// Error handler
app.use((err, req, res, next) => {
  logger.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => logger.info(`Server running on port ${PORT}`));
