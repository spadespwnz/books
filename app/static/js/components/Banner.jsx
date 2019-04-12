import React, { Component } from 'react';
import { Link } from 'react-router-dom'
import styles from './Banner.module.css';
export default class Banner extends Component {
    render() {

       return (
          <div className={styles.banner}>
            <div className={styles.banner__content}>
              <div className={styles.banner_left}>
                Title and logo
              </div>
              <div className={styles.banner_right}>
                <button>lol</button>
                links
                <Link to="/login">Login</Link>
              </div>
            </div>
          </div>
       )
    }
}
