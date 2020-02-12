const express = require('express')
const router = express.Router()
const User = require('../models/user')

// root_path/users handling

//Getting all
router.get('/', async (req, res) => {
    try {
        const users = await User.find()
        res.send(users)
    } catch(err) {
        res.status(500).json({message: err.message}) // status 500 means server error
    }
})

//Getting one
router.get('/:id', getUser, (req, res) => {
    res.json(res.user)
})

//Creating one
router.post('/', async (req, res) => {
    const user = new User({
        userName: req.body.userName,
        // query: req.body.query
    })
    try {
        const newUser = await user.save()
        res.status(201).json(newUser) // status 201 means successfully created an object
    } catch(err) {
        res.status(400).json({message: err.message})
    }
})

//Updating one
router.patch('/:id', getUser, async (req, res) => {
    if(req.body.userName !== null){
        res.user.userName = req.body.userName
    }
    // if(req.body.query !== null){
    //     res.user.query = req.body.query
    // }
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
    try {
        user = await User.findById(req.params.id)
        if(user === null){
            return res.status(404).json({message: 'Cannot find subscriber'})
        }
    } catch(err) {
        return res.status(500).json({message: err.message})
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