import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import styles from './Banner.module.css';
import {UserConsumer} from '../App';

export default class Banner extends Component {
    render() {

       return (
          <UserConsumer>
          {({loggedIn, name, onLogout}) => (
            <div className={styles.banner}>
              <div className={styles.banner__content}>
                <div className={styles.banner_left}>
                  {name}
                </div>
                <div className={styles.banner_right}>
                  <button onClick={onLogout}>lol</button>
                  links
                  <Link to="/login">Login</Link>
                </div>
              </div>
            </div>
          )}
          </UserConsumer>
       )
    }
}
