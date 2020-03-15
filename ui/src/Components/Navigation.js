import React, {Component} from 'react';
import {NavLink} from 'react-router-dom';


class Navigation extends Component {

    render() {
        return (
            <div>
                <NavLink to="/">
                    <button >Login</button>
                </NavLink>
                <NavLink to="/signup">
                    <button >Signup</button>
                </NavLink>
            </div>
        )
    }
}
export default Navigation;