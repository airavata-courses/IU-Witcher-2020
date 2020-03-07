import React, {Component} from 'react';
import axios from 'axios';
import '../App.css'

class Login extends Component {

    constructor(props) {
        super(props);
        this.state = {
            login: true,
            features: false,
            uname: "",
            password: "",
            search: "Bloomington Indiana USA KIND",
            prediction: "",
            history:""

        }
        this.setUsername = this.setUsername.bind(this);
        this.setPassword = this.setPassword.bind(this);
        this.login = this.login.bind(this);
        this.setSearch = this.setSearch.bind(this);
        this.history=this.history.bind(this);
    }

    setUsername = (event) => {
        this.setState({uname: event.target.value})
    }

    setPassword = (event) => {
        this.setState({password: event.target.value})
    }

    setSearch = (event) => {
        this.setState({search: event.target.value})
    }

    search = (event) => {
        event.preventDefault();
        axios.get('http://api_gate/data?search=' + this.state.search,{
            headers: {
                'Access-Control-Allow-Origin': '*',
            }
        })
            .then((response) => {
            // handle success
            console.log(response);
            this.setState({prediction: response.data})

        }).catch(function(error) {
            // handle error
            console.log(error);
        });

    }

    login = (event) => {
        event.preventDefault();

        // axios.post('http://127.0.0.1:5000/', {
        //     uname: this.state.uname,
        //     password: this.state.password
        // })
        //     .then((response) => {
        //         console.log(response);
        //     }, (error) => {
        //         console.log(error);
        //     });

        axios.get('http://api_gate?uname=' + this.state.uname + '&password=' + this.state.password).then((response) => {
            // handle success1
            console.log(response);
            if (response.data === 'Successfully logged in') {
                this.setState({features: true, login: false})
                alert('Successfully logged in')
            } else {
                alert('Error: Incorrect Username or Password')
            }

        }).catch(function(error) {
            // handle error
            console.log(error);
        }).then(function() {

            // always executed
        });

    }

    history=(event)=>{
        event.preventDefault()

        axios.get('http://apigateway/history')
            .then((response) => {
            // handle success
            console.log(response);
            this.setState({history:response.data})

        }).catch(function(error) {
            // handle error
            console.log(error);
        }).then(function() {

            // always executed
        });
    }

    render() {
        let logindiv = null;
        if (this.state.login) {
            logindiv = (<center>
                <form onSubmit={this.login}>
                    Login
                    <br/>
                    UserName:
                    <input type='text' name='uname' onChange={this.setUsername} required="required"/>
                    <br/>
                    PassWord:
                    <input type='text' name='password' onChange={this.setPassword} required="required"/>
                    <br/>
                    <input type='submit'/>
                </form>
            </center>)
        }

        let features = null;
        if (this.state.features) {
            features = (<center>
                Welcome {this.state.uname}
                <br/>
                <br/>
                <form onSubmit={this.search}>
                    Search:
                    <select name='search' onChange={this.setSearch} required="required">
                        <option value='Bloomington Indiana USA KIND'>
                            Bloomington Indiana USA KIND</option>
                        <option value='Indianapolis Indiana USA KIND'>Indianapolis, Indiana, USA, KIND </option>
                        <option value='Boston MA USA KBOX'>Boston, MA, USA, KBOX</option>
                        <option value='Cleveland OHIO USA KCLE'>Cleveland, OHIO, USA, KCLE</option>
                        <option value='Tucson Arizona USA KEMX'>Tucson, Arizona, USA, KEMX</option>
                    </select>
                    <input type='submit'></input>
                </form>

                <div className={'prediction'}>
                    <br/>
                    <br/> {this.state.prediction}
                    <img src='https://akiailzke76qae2cesgq-dump.s3.amazonaws.com/mytestfile'/>
                </div>
                <br/>

                <button>
                    <button onClick={this.history}>Check Session</button>
                    {this.state.history}
                </button>
            </center>)
        }

        return (<div className="App">
            {logindiv}
            {features}
        </div>);
    }
}

export default Login;
