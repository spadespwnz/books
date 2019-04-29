import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import {Redirect } from 'react-router-dom';
import styles from './Banner.module.css';
import {UserContext} from '../UserContext';
import SearchBar from './SearchBar'

export default class Banner extends Component {
    constructor(props){
      super(props)
      this.redirectToRegister = false;
      this.state = {};
      this.toRegisterPage = this.toRegisterPage.bind(this)
    }
    componentDidUpdate(){
      this.redirectToRegister = false;
    }
    toRegisterPage(){
      this.forceUpdate();
      this.redirectToRegister = true;

    }
    render() {
      if (this.redirectToRegister){
        return <Redirect to='/register' />
      }
       return (
          <UserContext.Consumer>
          {( {loggedIn, name, onLogout, onLogin} ) => (

            <div className={styles.banner}>
              <div className={styles.banner__content}>
                <div className={styles.banner_left}>
                  <p>Alexandria</p>

                </div>
                <div className={styles.banner_right}>
                  <div className={styles.banner_button_row}>
                    { loggedIn && <span className={styles.banner_button_row__item}>{name}</span>}
                    { loggedIn ? (
                      <button className={styles.banner_button_row__item+" btn btn-outline-secondary btn-sm"} onClick={onLogout}>Logout</button>
                    ) : (
                      <span>
                        <button className={styles.banner_button_row__item+" btn btn-outline-secondary btn-sm"} onClick={onLogin}>Login</button>
                        <button className={styles.banner_button_row__item+" btn btn-outline-secondary btn-sm"} onClick={
                          this.toRegisterPage
                        }>Register</button>
                      </span>
                    )}
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
