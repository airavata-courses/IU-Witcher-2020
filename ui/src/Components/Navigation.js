import React, {Component} from 'react';
import {NavLink} from 'react-router-dom';
import Button from 'react-bootstrap/Button'

class Navigation extends Component {

    render() {
        return (
            <div>
                <NavLink to="/">
                    <Button >Login</Button>
                </NavLink>
                <NavLink to="/signup">
                    <Button >Signup</Button>
                </NavLink>
            </div>
        )
    }
}
export default Navigation;