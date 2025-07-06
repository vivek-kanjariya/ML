const express = require('express');
const router = express.Router();
const predictController = require('../controllers/predictController');

// POST /api/predict
router.post('/', predictController.predict);

module.exports = router;
