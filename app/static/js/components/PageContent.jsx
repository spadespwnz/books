import React, { Component } from 'react';
import styles from './PageContent.module.css';
export default class PageContent extends Component {
    render() {

       return (
          <div class={styles.page}>
            <div class={styles.content}>
              {this.props.children}
            </div>
          </div>
       )
    }
}
