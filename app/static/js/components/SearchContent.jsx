import React, { Component } from 'react';
import API from '../api'
import {Redirect } from 'react-router-dom';

export default class SearchContent extends Component {
    constructor(props){
      super(props)

      this.state = {
        bookList:[],
        search:"",
      }
    }
    componentDidMount(){

      const { search_text } = this.props.match.params

      var books = []
      API.get(`/book/search/${search_text}`)
        .then(res => {
          for (var i in res.data){
            books.push(JSON.parse(res.data[i]))
            books[i].authorList=[]
            for (var j in books[i].authors){
              books[i].authorList.push(books[i].authors[j].key)
            }
          }
          this.setState({bookList:books,search:search_text})
        })
    }
    render(){
      return (
        <div>
          <h1>{this.state.search}</h1>
          <ul>
            {this.state.bookList.map((item,index) =>

                <li key={item.key.$oid}>{item.title}---{item.subtitle}--{item.authorList}</li>
                //<span>{item.title} {item.subtitle} {item.authors}</span>

            )}
          </ul>
        </div>
      )
    }
}
