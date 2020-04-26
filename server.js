require('dotenv').config() //load all environment variables from .env
const express = require('express')
const bodyParser = require('body-parser') //middleware for reading html from node
const cors = require('cors')
const app = express()
const mongoose = require('mongoose')
const usersRouter = require('./routes/users-sync')
// const usersRouter = require('./dbstatic')

// const historiesRouter = require('./routes/histories')

//db connection
// mongoose.connect(
//     'mongodb+srv://guest:iuwitcher2020@cluster0-eqjxv.mongodb.net/ads-project?retryWrites=true&w=majority',
//     {useNewUrlParser: true}
// )
// const db = mongoose.connection
// db.on('error', err => console.log(err))
// db.once('open', () => console.log('Connected to database!'))

/* MIDDLEWARES */
//Adding middleware to express using 'use' method
//Place middleware code before handlers
//'urlencoded' tells bodyParser to extract data from <form> element and add them to the 'body' property in request object

app.use(bodyParser(), cors())
express.json()
app.use(express.json())

app.use('/', usersRouter) //anything with the route 'root/users/anything/here' will go to usersRouter

// app.use('/histories', historiesRouter)

//handlers
app.listen(process.env.PORT || 4321, function() {
  console.log('Server started on port 4321')
})