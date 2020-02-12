const express = require('express')
const router = express.Router()
const History = require('../models/history')
const User = require('../models/user')

//Getting one
router.get('/', async (req, res) => {
    try {
        const history = await History.find({userName: req.body.userName})
        res.send(history)
    } catch(err) {
        res.status(500).json({message: err.message})
    }
})

//Creating one
router.patch('/', (req, res) => {
    try {
        const updatedHistory = History.find({userName: req.body.userName})
        res.status(200).json(updatedHistory)
    } catch(err) {
        res.status(500).json({message: err.message})
    }
})

module.exports = router