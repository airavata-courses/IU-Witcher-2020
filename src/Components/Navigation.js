import React,{Component} from 'react';
import {NavLink} from 'react-router-dom';


class Navigation extends Component {


    render() {
        return (
            <div>
                <center>


                <NavLink to="/">
                    <button >Login</button>
                </NavLink>
                <NavLink to="/signup">
                    <button >Signup</button>
                </NavLink>

                </center>

            </div>
        )
    }
}
export default Navigation;