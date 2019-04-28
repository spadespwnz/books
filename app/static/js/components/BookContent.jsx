import React, { Component } from 'react';
import API from '../api'
import {Redirect } from 'react-router-dom';

export default class BookContent extends Component {
    constructor(props){
      super(props)
      this.state = {...this.props.match.params};
      console.log(this.state)
    }
    updateBookData(){
      API.get('/book/id/'+this.state.book_id)
        .then(res => {
          console.log(res.data)
          const data = JSON.parse(res.data)
          console.log(data)
        })
    }
    componentDidMount(){
      this.updateBookData()
    }
    componentDidUpdate(){
      this.setState({book_id:this.props.match.params.book_id})
      this.updateBookData()
    }
    shouldComponentUpdate(nextProps, nextState){
      if (this.state.book_id == nextProps.match.params.book_id){
        return false;
      }
      return true;
    }
    render(){
      return (
        <div>
          {this.state.book_id}
        </div>
      )
    }
}
