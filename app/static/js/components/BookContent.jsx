import React, { Component } from 'react';
import API from '../api'
import {Redirect } from 'react-router-dom';
import styles from './BookContent.module.css';
import BookInteract from './BookInteract.jsx'

export default class BookContent extends Component {
    constructor(props){
      super(props)
      this.state = {...this.props.match.params};
    }
    urlChange(id){
      this.setState({book_id:id, book_data:null})
    }
    updateBookData(){
      console.log(this.state.loaded_book+"---"+this.state.book_id)
      if (this.state.loaded_book == this.state.book_id && this.state.loaded_book !== undefined){
        return;
      }
      API.get('/book/id/'+this.state.book_id)
        .then(res => {
          const data = JSON.parse(res.data)
          this.setState({book_data:data, loaded_book:this.state.book_id})
        })
    }
    componentDidMount(){
      this.updateBookData()
    }
    componentDidUpdate(){
      this.updateBookData()

    }

    shouldComponentUpdate(nextProps, nextState){

      if (this.state.book_id != nextProps.match.params.book_id){
        console.log("URL CHANGE")
        this.urlChange(nextProps.match.params.book_id);
        return false;
      }
      return true;
    }

    render(){
      console.log(this.state)
      let title = "";
      let subtitle = null;
      if (this.state.book_data){
        title = this.state.book_data["title"]
        subtitle = this.state.book_data["subtitle"]
      }

      return (
        <div className={styles.component}>
          <div className={styles.side_column}>
            {this.state.book_data && this.state.book_data["isbn_10"] && (
              <img src={"http://covers.openlibrary.org/b/isbn/"+this.state.book_data["isbn_10"][0]+"-M.jpg"} />
              )
             }
          </div>
          <div className={styles.main_column}>
            <span className={styles.main_column__title}>{title}</span>
            <span className={styles.main_column__title}>{subtitle}</span>
            <div className={styles.book_info}>
              Some Info
            </div>
            <div className={styles.book_interact}>
              <BookInteract id={this.state.book_id}/>
            </div>

            <div className={styles.main_column__content}>
              Some stuff
            </div>
          </div>
        </div>
      )
    }
}
