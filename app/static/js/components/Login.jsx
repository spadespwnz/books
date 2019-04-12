import React, { Component } from 'react';
export default class Login extends Component {
  constructor(props){
    super(props)

    this.state = {
      email_or_username: "",
      password: "",
      submitted: false
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  validateForm(){
    return this.state.email.length > 0 && this.state.password.length > 0;
  }

  handleChange(e){
    const {name, value} = e.target;
    this.setState({ [name]: value});
  }

  handleSubmit(e){
    e.preventDefault();
    const {username, password} = this.state;
    this.setState({submitted: true})
  }
  render() {

     return (
      <div>
        <h1>Login</h1>
        <form onSubmit={this.handleSubmit}>
          <div class="form-group">
            <label>
              Username or Email:
              <input class="form-control" type="text" name="email_or_username" value={this.state.email_or_username} onChange={this.handleChange} />
            </label>
          </div>
          <div class="form-group">
            <label>
              Password
              <input class="form-control" type="password" name="password" value={this.state.password} onChange={this.handleChange} />
            </label>
          </div>
        </form>
      </div>

     )
  }
}
