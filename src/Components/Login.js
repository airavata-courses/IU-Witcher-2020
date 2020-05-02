import React, {Component} from 'react';
import axios from 'axios';
import '../App.css'

class Login extends Component {

    constructor(props) {
        super(props);
        this.state = {
            login: true,
            features: false,
            username: "",
            password: "",
            search: "Bloomington Indiana USA KIND",
            prediction: [],
            history:""

        }
        this.setUsername = this.setUsername.bind(this);
        this.setPassword = this.setPassword.bind(this);
        this.login = this.login.bind(this);
        this.setSearch = this.setSearch.bind(this);

    }

    setUsername = (event) => {
        this.setState({username: event.target.value})
    }

    setPassword = (event) => {
        this.setState({password: event.target.value})
    }

    setSearch = (event) => {
        this.setState({search: event.target.value})
    }

    search = (event) => {
        event.preventDefault();
        alert('Your Request is Successfully Submitted');
        axios.get('http://149.165.171.22:30000/data?username='+ this.state.username+'&search=' + this.state.search)
            .then((response) => {
            // handle success
            console.log(response);
            this.setState({prediction: this.state.prediction.concat(response.data)})

        }).catch(function(error) {
            // handle error
            console.log(error);
        });

    }

    login = (event) => {
        event.preventDefault();

        // axios.post('http://127.0.0.1:5000/', {
        //     username: this.state.username,
        //     password: this.state.password
        // })
        //     .then((response) => {
        //         console.log(response);
        //     }, (error) => {
        //         console.log(error);
        //     });

        axios.get('http://149.165.171.22:30000/?username=' + this.state.username + '&password=' + this.state.password).then((response) => {
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
        })//.then(function() {

            // always executed
        //});

    }


    render() {

        let logindiv = null;
        if (this.state.login) {
            logindiv = (<center>
                <div  style={{backgroundColor:"white"}}>For guest user: UserName = Guest and Password = Guest </div>
                <br/> 
                <form onSubmit={this.login}>
                <div >| <button>Login</button>  |</div>
                    <br/>

                    <input type='text' placeholder={'Username'} name='username' onChange={this.setUsername} required="required"/>
                    <br/>

                    <input type='password' placeholder={'Password'} name='password' onChange={this.setPassword} required="required"/>
                    <br/>
                    <input type='submit'/>
                </form>
            </center>)
        }

        let features = null;
        if (this.state.features) {
            features = (<center>
              <h3>  Welcome {this.state.username} </h3>
                <br/>
                <br/>
                <form onSubmit={this.search}>
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
                    <br/><b>Weather Forecasting Results:</b>
                    <br/> 
                    <ol>
                    {this.state.prediction.map(results => <li>{results}</li>)}
                    </ol>
                    <br/>

                </div>
                <br/>


                
            </center>)
        }

        return (<div className="App">
            {logindiv}
            {features}
        </div>);
    }
}

export default Login;
