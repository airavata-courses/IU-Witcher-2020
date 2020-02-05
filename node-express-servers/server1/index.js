//change port in windows using 'set PORT=port_number'

const Joi = require('joi') //returns a class, so capital
const express = require('express') //returns a function

//call the imported fn and call it app, app has get, post, put, delete methods
const app = express()
// const request = require('request')
// const server = require('http').createServer(app)
// const io = require('socket.io')(server)
// const bodyParser = require('body-parser')

// express.json() returns a middleware, we use it using app.use
app.use(express.json())

const courses = [
    {id: 1, name: 'course 1'},
    {id: 2, name: 'course 2'},
    {id: 3, name: 'course 3'}
]

app.get('/', (req, res) => {
    res.send('Hello world!!!')
})

app.get('/', (req, res) => {
    res.send('Hello world!!!')
})

app.get('/api/courses', (req, res) => {
    res.send(courses)
})

// app.get('/listen/port2', (req, res) => {
//     request({
//         uri: 'localhost:3001/port2',
//         method: 'GET',
//         timeout: 10000
//     }, (err, response, body) => {
//         console.log(body)
//         res.send(body)
//     })
// })

// id is a route parameter so defined with colon
// req.params.id is used to get the value of id
app.get('/api/courses/:id', (req, res) => {
    let course = courses.find(c => c.id === parseInt(req.params.id))
    if(!course) res.status(404).send('No course with this id found') //404 error
    res.send(course)
})

// query string params occur after ?
app.get('/api/courses/:year/:month', (req, res) => {
    res.send(req.query) // if we go to url "/api/courses/2019/1?sortBy=name", req.query is {sortBy: name}
})

app.post('/api/courses', (req, res) => {

    const schema = {
        name: Joi.string().min(3).required()
    }
    const result = Joi.validate(req.body, schema)
    //
    if(result.error){
        res.send(result.error.details)
    }

    const course = {
        id: courses.length + 1,
        name: req.body.name
    }
    courses.push(course)
    res.send(course) // newly created objects are always sent back in response
})

// use port if defined
const port = process.env.PORT || 3000
app.listen(port, () => {
    console.log(`Listening to port ${port}`)
})


