require('dotenv').config() //load all environment variables from .env
const express = require('express')
const bodyParser = require('body-parser') //middleware for reading html from node
const app = express()
const mongoose = require('mongoose')
const usersRouter = require('./routes/users')

//db connection
mongoose.connect(process.env.DATABASE_URL, {useNewUrlParser: true})
const db = mongoose.connection
db.on('error', err => console.log(err))
db.once('open', () => console.log('Connected to database!'))

/* MIDDLEWARES */
//Adding middleware to express using 'use' method
//Place middleware code before handlers
//'urlencoded' tells bodyParser to extract data from <form> element and add them to the 'body' property in request object
app.use(bodyParser.urlencoded({extended: true}))
express.json()
app.use(express.json())

app.use('/users', usersRouter) //anything with the route 'root/users/anything/here' will go to usersRouter

//handlers
app.listen(process.env.PORT || 4321, function() {
  console.log('Server started on port 4321')
})

// const users = [
//     {id: 1, name: 'user 1'},
//     {id: 2, name: 'nana 2'},
//     {id: 3, name: 'saa 3'}
// ]
//
// app.get('/home', (req, res) => {
//     res.send('homepage')
// })
//
// app.get('/', (req, res) => {
//     res.sendFile(__dirname + '/index.html')
// })
//
// app.get('/user/:id', (req, res) => {
//     let user = users.find(u => u.id === parseInt(req.params.id))
//     if(!user) res.status(404).send('No user with this id found') //404 error
//     res.send(user)
// })
//
// app.post('/addUser', (req, res) => {
//     res.send('User added')
// })