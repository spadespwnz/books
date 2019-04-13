import React, { Component } from 'react';
import API from '../api'
import styles from './Register.module.css';
export default class Register extends Component {
  constructor(props){
    super(props)

    this.state = {
      email: "",
      username: "",
      password: "",
      submitted: false,
      validUsername: null,
      validEmail: null,
      validPassword: null,
    };
    this.invalidUsernameReason = "";
    this.invalidEmailReason = "";

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.verifyUsername = this.verifyUsername.bind(this);
    this.verifyEmail = this.verifyEmail.bind(this);
    this.verifyPassword = this.verifyPassword.bind(this);
    this.drop = this.drop.bind(this);
    this.passwordCheckTimeout = 0;
    this.emailCheckTimeout = 0;
    this.usernameCheckTimeout = 0;
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
  verifyPassword(e){
    const pattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/
    if (this.passwordCheckTimeout) clearTimeout(this.passwordCheckTimeout);
    this.passwordCheckTimeout = setTimeout(() =>{
      const {password} = this.state;
      if (!pattern.test(password)){
        this.setState({validPassword: false})
        return;
      }
      this.setState({validPassword: true})
    },1000)

  }
  verifyEmail(e){
    const pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (this.emailCheckTimeout) clearTimeout(this.emailCheckTimeout);
    this.emailCheckTimeout = setTimeout(() =>{
      const {username, email, password} = this.state;
      if (!pattern.test(email)){
        this.invalidEmailReason = "Invalid Email.";
        this.setState({validEmail: false})
        return;
      }
      const data = {username, email,password};
      API.post('/check_valid_email',data)
        .then(res => {
          console.log(res)
          this.setState({validEmail: res.data.data})
          this.invalidEmailReason = res.data.reason;
      })
    },1000)
  }

  verifyUsername(e){
    const pattern = /^[a-zA-Z0-9_]{3,20}$/;
    if (this.usernameCheckTimeout) clearTimeout(this.usernameCheckTimeout);
    this.usernameCheckTimeout = setTimeout(() =>{
      const {username, email, password} = this.state;
      if (!pattern.test(username)){
        this.setState({validUsername: false})
        this.invalidUsernameReason = "Must contain only letters, numbers, and underscores.";
        return;
      }
      const data = {username, email,password};
      API.post('/check_valid_username',data)
        .then(res => {
          console.log(res)
          this.setState({validUsername: res.data.data})
          this.invalidUsernameReason = res.data.reason;
      })
    },1000)
  }
  handleChange(e){
    const {name, value} = e.target;
    this.setState({ [name]: value});
  }

  handleSubmit(e){
    e.preventDefault();
    const {username, email, password} = this.state;
    const data = {username, email,password};
    this.setState({submitted: true})

    API.post('/register',data)
      .then(res => {
        console.log(res)
      })

  }
  render() {

     return (
      <div className={styles.component}>
        <h1>Sign Up</h1>
        <form className={styles.form} onSubmit={this.handleSubmit}>
          <div className={styles.form_field+" form-group "}>
            <label className={styles.label}>
              Email:
              <input className={" form-control " +(this.state.validEmail == null?"":this.state.validEmail || " is-invalid ") + (this.state.validEmail && " is-valid ")}
              type="email" name="email" value={this.state.email} onChange={(e) => {this.handleChange(e); this.verifyEmail(e)}}
              onBlur={this.verifyEmail}/>
              {this.state.validEmail==false ?
                <small id="usernameHelp" class="text-danger">
                  {this.invalidEmailReason}
                </small> :  null}
            </label>
          </div>
          <div className={styles.form_field+" form-group "}>
            <label className={styles.label}>
              Username:
              <input className={"form-control " +(this.state.validUsername == null?"":this.state.validUsername || " is-invalid ") + (this.state.validUsername && " is-valid ")}
              type="text" name="username" value={this.state.username} onChange={(e) => {this.handleChange(e); this.verifyUsername(e)}}
              onBlur={this.verifyUsername}/>
              {this.state.validUsername==false ?
                <small id="usernameHelp" class="text-danger">
                  {this.invalidUsernameReason}
                </small> :  null}
            </label>
          </div>
          <div className={styles.form_field+" form-group "}>
            <label className={styles.label}>
              Password
              <input className={"form-control " +(this.state.validPassword == null?"":this.state.validPassword || " is-invalid ") + (this.state.validPassword && " is-valid ")}
              onBlur={this.verifyPassword} type="password" name="password" value={this.state.password} onChange={ (e) => {this.handleChange(e); this.verifyPassword(e)} } />
              {this.state.validPassword==false ?
                <small id="passwordHelp" class="text-danger">
                  Password must be 8 or more characters, and contain one number.
                </small> :  null}
            </label>
          </div>
          <button type="submit" class="btn btn=primary">Sign Up</button>
          <button type="button" class="btn btn=primary" onClick={this.drop}>Drop</button>
        </form>
      </div>

     )
  }
}
