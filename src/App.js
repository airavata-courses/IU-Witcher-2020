import React,{Component} from 'react';
import Login from './Components/Login';
import Signup from './Components/Signup';

import './App.css';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            login: true,
            signup:false
        }
        this.signupButton=this.signupButton.bind(this);

    }

    signupButton=(event)=>{
      this.setState({signup:!this.state.signup})
    }
    render() {
        let signup_form=null
        if(this.state.signup){
          signup_form=<Signup/>
        }
        return (

            <div className="App">

                <div>
                    <button onClick={this.signupButton}> Signup Tab </button>
                    <br/>
                    {signup_form}
                    <br/>
                </div>

              <br/>
                <br/>


              <center>
                      <Login/>
                </center>

            </div>
        );
    }

}
export default App;
