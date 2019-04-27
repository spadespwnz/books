import React, { Component } from 'react';
import API from '../api'
import Select from 'react-select'
import {Redirect } from 'react-router-dom';
import AsyncSelect from 'react-select/lib/Async';
import styles from './SearchBar.module.css';

const searchBarStyles = {
  option: (provided, state)  => ({
    ...provided,
    whiteSpace: "pre-wrap",
  })
}
export default class Register extends Component {
  constructor(props){
    super(props)

    this.state = {
      words:[],
      redirectToBook: false,
      redirectToSearch: false,
      bookId: null,
    }
    this.searchText = ""
    this.inputChange = this.inputChange.bind(this)
    this.change = this.change.bind(this)
    this.loadOptions = this.loadOptions.bind(this)
    this.keyDown = this.keyDown.bind(this)
    this.searchTimeout = 0;
  }
  componentDidUpdate(){
    if (this.state.redirectToBook) this.setState({redirectToBook:false})
    if (this.state.redirectToSearch) this.setState({redirectToSearch:false})

  }
  inputChange(value, {action}){

  }
  change(value, {action}){
    this.setState({redirectToBook: true, bookId: value.key.$oid})
  }
  keyDown(keyEvent){
    if (keyEvent.key == "Enter"){
      if (!keyEvent.getModifierState()){
        this.setState({redirectToSearch: true})
      }
    }

  }
  loadOptions(input, callback){
    input = input.replace(" ","_")
    this.searchText = input;
    if (this.searchTimeout) clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      var books = []
      API.get(`/book/search/${input}`)
        .then(res => {

          for (var i in res.data){
            books.push(JSON.parse(res.data[i]))
            books[i].authorList=[]
            books[i].label = `${books[i].title}\n${books[i].subtitle}\n`
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
     if (this.state.redirectToSearch){
       return <Redirect to={'/book/search/'+this.searchText} />
     }
    return (
      <div className={"searchBar "+styles.component}>
        {
          <AsyncSelect
            styles={searchBarStyles}
            loadOptions={this.loadOptions}
            onChange={this.change}
            onKeyDown={this.keyDown}
            onInputChange={this.inputChange}/>

        }

      </div>
    )
  }
}
