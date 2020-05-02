import React, {Component} from 'react';
import axios from 'axios';
class Signup extends Component {

    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password:""
        }
        this.setUsername = this.setUsername.bind(this);
        this.setPassword = this.setPassword.bind(this);
        this.signup = this.signup.bind(this);
    }

    setUsername = (event) => {
        this.setState({username: event.target.value})
    }

    setPassword = (event) => {
        this.setState({password: event.target.value})
    }

    signup = (event) => {
        event.preventDefault()

        // axios.post('http://127.0.0.1:5000/', {
        //     uname: this.state.uname,
        //     password: this.state.password
        // })
        //     .then((response) => {
        //         console.log(response);
        //     }, (error) => {
        //         console.log(error);
        //     });


        axios.get('http://149.165.171.22:30000/signup?username='+this.state.username+'&password='+this.state.password)
            .then( (response)=> {
                // handle success
                console.log(response);
                if(response.data==='Successfully Created User'){
                    alert("Registered Successfully")
                }
                else {
                    alert("User Already exists")
                }

            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
            .then(function () {

                // always executed
            });



    }

    render() {


        return (
            <div>
            <center>

            <div >
                <form onSubmit={this.signup}>
                   <div > <button> Signup</button>  </div>
                    <br/>
                     <input type='text' name='username' onChange={this.setUsername} required/>
                    <br/>
                     <input type='text' name='password' onChange={this.setPassword} required/>
                    <br/>
                    <input type='submit'></input>
                </form>
            </div>

            </center>

            </div>
    );

    }
}

export default Signup;
