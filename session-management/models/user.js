const mongoose = require('mongoose')
const Schema = mongoose.Schema;

const usersSchema = new Schema({
    userName: {
        type: String,
        required: true,
        unique: true
    },
    search: [{
        type: String
    }]
})

module.exports = mongoose.model('user', usersSchema)