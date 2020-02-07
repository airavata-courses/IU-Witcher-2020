import React,{Component} from 'react';
import axios from 'axios';
class Login extends Component{

    constructor(props) {
        super(props);
        this.state={
            login: true,
            features: false,
            uname: "",
            password:""
        }
        this.setUsername=this.setUsername.bind(this);
        this.setPassword=this.setPassword.bind(this);
        this.login=this.login.bind(this);
    }

    setUsername=(event)=>{
        this.setState({uname:event.target.value})
    }

    setPassword=(event)=>{
        this.setState({password:event.target.value})
    }

    login=(event)=>{
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

        axios.get('http://127.0.0.1:5000/?uname='+this.state.uname+'&password='+this.state.password)
            .then( (response)=> {
                // handle success
                console.log(response);
                if(response.data==='Successfully logged in'){
                    this.setState({features:true,login:false})
                    alert('Successfully logged in')
                }
                else {
                    alert('Error: Incorrect Username or Password')
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
        let logindiv = null;
        if(this.state.login) {
            logindiv = (
                <center>

                    <form onSubmit={this.login}>

                        Login
                        <br/>
                        UserName: <input type='text' name='uname' onChange={this.setUsername} required/>
                        <br/>
                        PassWord: <input type='text' name='password' onChange={this.setPassword} required/>
                        <br/>
                        <input type='submit'></input>
                    </form>
                </center>
                    )
                    }

        let features = null;
        if(this.state.features) {
            features = (
                <center>
                    Welcome {this.state.uname} <br/>
                    <button>
                        Retrive Data
                    </button>
                    <br/>
                    <button>
                        Check Session

                    </button>

                </center>
            )
        }

        return (
            <div className="App">
                {logindiv}
                {features}
            </div>
        );
    }
}

export default Login;
