import React,{Component} from 'react';
import Login from './Components/Login';
import Signup from './Components/Signup';
import Navigation from './Components/Navigation';
import { BrowserRouter, Route, Switch } from "react-router-dom";

import './App.css';

class App extends Component {
    render() {
        return (
            <BrowserRouter>
                <div>
                    <Navigation/>
                    <Switch>
                        <Route path="/" component={Login} exact/>
                        <Route path="/signup" component={Signup}/>
                    </Switch>
                </div>
            </BrowserRouter>
        );
    }

}


export default App;
