import React, { Component } from 'react';
import styles from './Banner.module.css';
export default class Banner extends Component {
    render() {

       return (
          <div className={styles.banner}>
            <div className={styles.banner__content}>Banner</div>
          </div>
       )
    }
}
