import React,{Component} from 'react';
import axios from 'axios';
class Signup extends Component{

    constructor(props) {
        super(props);
        this.state={
            uname: "",
            password:"",
            signup_form:true
        }
        this.setUsername=this.setUsername.bind(this);
        this.setPassword=this.setPassword.bind(this);
        this.signup=this.signup.bind(this);
    }

    setUsername=(event)=>{
        this.setState({uname:event.target.value})
    }

    setPassword=(event)=>{
        this.setState({password:event.target.value})
    }

    signup=(event)=>{
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

        axios.get('http://127.0.0.1:5000/signup?uname='+this.state.uname+'&password='+this.state.password)
            .then( (response)=> {
                // handle success
                console.log(response);
                if(response.data==='Successfully Created User'){
                    this.setState({signup_form:false})
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


    render(){

        let signupdiv=null;
        if(this.state.signup_form){
            signupdiv=(
                <center>

                    <div >
                        <form onSubmit={this.signup}>
                            Signup
                            <br/>
                            UserName: <input type='text' name='uname' onChange={this.setUsername} required/>
                            <br/>
                            PassWord: <input type='text' name='password' onChange={this.setPassword} required/>
                            <br/>
                            <input type='submit'></input>
                        </form>

                    </div>

                </center>
            )

        }
        return (
            <div>
                {signupdiv}
            </div>
        );
    }
}

export default Signup;
