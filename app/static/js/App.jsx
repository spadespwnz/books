import React, {Component} from 'react';
import { BrowserRouter, Route, Redirect, browserHistory, withRouter } from 'react-router-dom';
import Home from './components/Home';
import Clock from './components/Clock'
import Banner from './components/Banner'
import Login from './components/Login'
import Register from './components/Register'
import PageContent from './components/PageContent'
import SearchContent from './components/SearchContent'
import API from './api'
import {UserContext} from './UserContext'

class App extends Component{
  constructor(props){
    super(props)
    this.state = {
      toLogin: false,
      loggedIn: false,
      name: "",
    };

    this.handleLogin = this.handleLogin.bind(this)
    this.handleLogout = this.handleLogout.bind(this)
    this.fetchUserData = this.fetchUserData.bind(this)
  };
  componentDidMount(){
    this.fetchUserData()
  }

  handleLogout(){
    API.get('/logout')
      .then(res => {
        console.log(res)
      })

    this.setState({loggedIn: false})
  }
  handleLogin(){
    this.props.history.push('/login')
    this.setState({loggedIn: false, toLogin: true})
  }
  fetchUserData(){
    API.get('/check_token')
      .then(res => {

        if (res.data.code==2000){
          this.setState({loggedIn: false, name: ""})
        }
        if (res.data.code==6){

          this.setState({loggedIn: true, name: res.data.data.username})
        }
      })
  }
  render(){
    return(
        <UserContext.Provider value={{ loggedIn:this.state.loggedIn, name:this.state.name,onLogout: this.handleLogout, onLogin: this.handleLogin, fetchUserData: this.fetchUserData}}>
          <div>
          <Route component={Banner} />
          {/*
          <Route path='/' component={Home} />
          <Route path='/' render={(props) => <Home text="Test" {...props} />} />
          */}

          <PageContent path='/' component={PageContent}>
            <div>
              <Route exact path='/' component={Clock} />
              <Route path='/book/search/:search_text' component={SearchContent} />
              <Route path='/login' component={Login} />
              <Route path='/Register' component={Register} />
            </div>
          </PageContent>
         </div>
        </UserContext.Provider>

    )
  }
};

export default withRouter(App);
