import React, { Component } from 'react';
import styles from './Login.module.css';
import API from '../api'
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
    return this.state.email_or_username.length > 0 && this.state.password.length > 0;
  }

  handleChange(e){
    const {name, value} = e.target;
    this.setState({ [name]: value});
  }

  handleSubmit(e){
    e.preventDefault();
    if (!this.validateForm()) return;
    const {email_or_username, password} = this.state;
    const data = {email_or_username,password};
    API.post('/login',data)
      .then(res => {
        console.log(res)
      })
    this.setState({submitted: true})
  }
  render() {

     return (
      <div className={styles.component}>
        <h1>Login</h1>
        <form className={styles.form} onSubmit={this.handleSubmit}>
          <div className={styles.form_field+" form-group "}>
            <label className={styles.label}>
              Username or Email:
              <input class="form-control" type="text" name="email_or_username" value={this.state.email_or_username} onChange={this.handleChange} />
            </label>
          </div>
          <div className={styles.form_field+" form-group "}>
            <label className={styles.label}>
              Password
              <input class="form-control" type="password" name="password" value={this.state.password} onChange={this.handleChange} />
            </label>
          </div>
          <button type="submit" class="btn btn=primary">Log In</button>
        </form>
      </div>

     )
  }
}
