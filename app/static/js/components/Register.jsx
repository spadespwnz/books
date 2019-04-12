import React, { Component } from 'react';
import API from '../api'
export default class Register extends Component {
  constructor(props){
    super(props)

    this.state = {
      email: "",
      username: "",
      password: "",
      submitted: false,
      validUsername: null,
      validEmail: null
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.verifyUsername = this.verifyUsername.bind(this);
    this.verifyEmail = this.verifyEmail.bind(this);
    this.drop = this.drop.bind(this);
  }

  validateForm(){
    return this.state.email.length > 0 && this.state.password.length > 0;
  }

  drop(e){
    API.get('/drop')
      .then(res =>{
        console.log(res)
      })
  }

  verifyEmail(e){
    const pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const {username, email, password} = this.state;
    if (!pattern.test(email)){
      this.setState({validEmail: false})
      return;
    }
    const data = {username, email,password};
    API.post('/check_valid_email',data)
      .then(res => {
        this.setState({validEmail: res.data.data})
      })
  }

  verifyUsername(e){
    const pattern = /^[a-zA-Z0-9_]{3,20}$/;

    const {username, email, password} = this.state;
    if (!pattern.test(username)){
      this.setState({validUsername: false})
      return;
    }
    const data = {username, email,password};
    API.post('/check_valid_username',data)
      .then(res => {
        this.setState({validUsername: res.data.data})
      })
  }
  handleChange(e){
    const {name, value} = e.target;
    this.setState({ [name]: value});
  }

  handleSubmit(e){
    e.preventDefault();
    const {username, email, password} = this.state;
    const data = {username, email,password};
    console.log(data)
    this.setState({submitted: true})

    API.post('/register',data)
      .then(res => {
        console.log(res)
      })

  }
  render() {

     return (
      <div>
        <h1>Sign Up</h1>
        <form onSubmit={this.handleSubmit}>
          <div class="form-group">
            <label>
              Email:
              <input className={"form-control " +(this.state.validEmail == null?"":this.state.validEmail || " is-invalid ") + (this.state.validEmail && " is-valid ")}
              type="email" name="email" value={this.state.email} onChange={this.handleChange}
              onBlur={this.verifyEmail}/>
            </label>
          </div>
          <div class="form-group">
            <label>
              Username:
              <input className={"form-control " +(this.state.validUsername == null?"":this.state.validUsername || " is-invalid ") + (this.state.validUsername && " is-valid ")}
              type="text" name="username" value={this.state.username} onChange={this.handleChange}
              onBlur={this.verifyUsername}/>
            </label>
          </div>
          <div class="form-group">
            <label>
              Password
              <input class="form-control" type="password" name="password" value={this.state.password} onChange={this.handleChange} />
            </label>
          </div>
          <button type="submit" class="btn btn=primary">Sign Up</button>
          <button type="button" class="btn btn=primary" onClick={this.drop}>Drop</button>
        </form>
      </div>

     )
  }
}
