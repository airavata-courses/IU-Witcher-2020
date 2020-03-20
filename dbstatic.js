// let thisuser = new Schema({
//     userName: {
//         type: String,
//         required: true,
//         unique: true
//     },
//     search: [{
//         type: String
//     }],
//     prediction: [{
//         temp: Number,
//         temp_min: Number,
//         temp_max: Number,
//         humidity: Number,
//         weather: String,
//         wind_speed: Number,
//         date_time: String
//     }]
// })

const express = require('express')
const router = express.Router()

let userHistory = []

router.get('/', (req, res) => {
    try {
        res.send(userHistory)
    } catch(err) {
        res.status(500).json({message: err.message}) // status 500 - server error
    }
})

module.exports = router