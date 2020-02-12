const express = require('express')
const router = express.Router()
const User = require('../models/user')

// root_path/users api

//Getting all
router.get('/', async (req, res) => {
    try {
        const users = await User.find()
        res.send(users)
    } catch(err) {
        res.status(500).json({message: err.message}) // status 500 - server error
    }
})

//Getting one
router.get('/:id', getUserFromQuery, (req, res) => {
    res.json(res.user)
})

//Creating one
router.post('/', async (req, res) => {
    console.log('POST CALL', req.body)
    const user = new User({
        userName: req.body.userName,
        search: [req.body.search],
        prediction: [{...req.body.prediction}]
    })
    try {
        const newUser = await user.save()
        res.status(201).json(newUser) // status 201 - successfully created an object
    } catch(err) {
        res.status(400).json({message: err.message})
    }
})

//Updating one
router.put('/', getUser, async (req, res) => {
    // console.log('PUT CALL', req.body)
    if(req.body.userName !== null){
        res.user.userName = req.body.userName
    }
    if(req.body.search !== null){
        res.user.search.push(req.body.search)
    }
    if(req.body.prediction !== null){
        res.user.prediction = [
            ...res.user.prediction,
            {...req.body.prediction}
        ]
    }
    try {
        const updatedUser = await res.user.save()
        res.json(updatedUser)
    } catch(err) {
        res.status(400).json({message: err.message})
    }
})

//Deleting one
router.delete('/:id', getUser, async (req, res) => {
    try {
        await res.user.remove()
        res.json({message: 'Deleted subscriber'})
    } catch(err) {
        res.status(500).json({message: err.message})
    }
})

//getUser middleware
async function getUser(req, res, next){
    let user
    // console.log('MIDDLEWARE REQ BODY', req.body)
    try {
        // user = await User.findById(req.params.id)
        user = await User.findOne({userName: req.body.userName})
        if(user === null){
            return res.status(404).json({message: 'Cannot find user'})
        }
    } catch(err) {
        return res.status(500).json({message: err.message})
    }
    res.user = user
    next()
}

//getUser middleware
async function getUserFromQuery(req, res, next){
    let user
    // console.log('MIDDLEWARE REQ BODY', req.body)
    try {
        user = await User.findOne({userName: req.params.id})
        if(user === null){
            return res.status(404).json({
                statusCode: 404,
                message: 'Cannot find user'
            })
        }
    } catch(err) {
        return res.status(500).json(err)
    }
    res.user = user
    next()
}

//
// const createUsers = async () => {
//     const user1 = new User({
//         userName: 'akshay'
//     })
//     await user1.save()
// }

module.exports = router