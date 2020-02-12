const mongoose = require('mongoose')

const usersSchema = new mongoose.Schema({
    userName: {
        type: String,
        required: true,
        unique: true
    },
    search: {
        type: String,
        required: true
    },
    prediction: {
        temp: Number,
        temp_min: Number,
        temp_max: Number,
        humidity: Number,
        weather: String,
        wind_speed: Number,
        date_time: String
    }
})

module.exports = mongoose.model('user', usersSchema)