import React, { Component } from 'react';
import API from '../api'
import {Redirect } from 'react-router-dom';
import {UserContext} from '../UserContext';

class BookInteract extends Component {
  constructor(props, context){
    super(props, context)
    this.addToReadList = this.addToReadList.bind(this)
    this.getList = this.getList.bind(this)
  }

  addToReadList(e){
    const data = {"id":this.props.id};
    API.post('/books/to_read_list/add',data)
      .then(res => {
        console.log(res)
      })
  }
  getList(e){
    const data = {"username":"qwe1"}
    API.post('/profile/to_read_list/get',data)
      .then(res => {
        console.log(res)
      })
  }
  render(){
    const buttons = []
    buttons.push(<button onClick={this.addToReadList}>^To-Read List^</button>)
    buttons.push(<button onClick={this.getList}>^GET^</button>)
    return(
      <div>
        {this.context.loggedIn ?
            <div>
              {buttons}
            </div>
            :
            "Must Login before adding to lists."}

      </div>
    )
  }
}

BookInteract.contextType = UserContext;
export default BookInteract;
