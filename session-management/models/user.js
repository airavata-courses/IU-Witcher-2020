const mongoose = require('mongoose')

const usersSchema = new mongoose.Schema({
    userName: {
        type: String,
        required: true,
        unique: true
    }
})

module.exports = mongoose.model('user', usersSchema)