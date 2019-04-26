import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import styles from './Banner.module.css';
import {UserContext} from '../UserContext';
import SearchBar from './SearchBar'

export default class Banner extends Component {

    render() {
       return (
          <UserContext.Consumer>
          {( {loggedIn, name, onLogout, onLogin} ) => (

            <div className={styles.banner}>
              <div className={styles.banner__content}>
                <div className={styles.banner_left}>
                  { loggedIn && <h2>{name}</h2>}
                </div>
                <div className={styles.banner_right}>
                  <div>
                    { loggedIn ? (
                      <button onClick={onLogout}>Logout</button>
                    ) : (
                      <button onClick={onLogin}>Login</button>
                    )}
                    links
                    <Link to="/login">Login</Link>
                  </div>
                  <SearchBar />
                </div>

              </div>
            </div>
          )}
          </UserContext.Consumer>
       )
    }
}
