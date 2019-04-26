import React, { Component } from 'react';
import API from '../api'
import Select from 'react-select'
import {Redirect } from 'react-router-dom';
import AsyncSelect from 'react-select/lib/Async';
import styles from './SearchBar.module.css';

export default class Register extends Component {
  constructor(props){
    super(props)

    this.state = {
      words:[],
      redirectToBook: false,
      bookId: null,
    }
    this.inputChange = this.inputChange.bind(this)
    this.change = this.change.bind(this)
    this.loadOptions = this.loadOptions.bind(this)
    this.searchTimeout = 0;
  }
  componentDidUpdate(){
    if (this.state.redirectToBook) this.setState({redirectToBook:false})

  }
  inputChange(value, {action}){

  }
  change(value, {action}){
    console.log(value)
    this.setState({redirectToBook: true, bookId: value.key.$oid})
  }
  loadOptions(input, callback){
    if (this.searchTimeout) clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      input = input.replace(" ","_")
      var books = []
      API.get(`/book/search/${input}`)
        .then(res => {

          for (var i in res.data){
            books.push(JSON.parse(res.data[i]))
            books[i].authorList=[]
            books[i].label = books[i].title
            for (var j in books[i].authors){
              books[i].authorList.push(books[i].authors[j].key)
            }
          }
          callback(books)
        })

    },1000)
  }

  render(){
    if (this.state.redirectToBook){
      return <Redirect to={'/book/id/'+this.state.bookId} />
     }
    return (
      <div className={"searchBar "+styles.component}>
        {
          <AsyncSelect

            loadOptions={this.loadOptions}
            onChange={this.change}
            onInputChange={this.inputChange}/>

        }

      </div>
    )
  }
}
