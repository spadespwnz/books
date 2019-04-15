import React, {Component} from 'react';
import { BrowserRouter, Route, hashHistory } from 'react-router-dom';
import Home from './components/Home';
import Clock from './components/Clock'
import Banner from './components/Banner'
import Login from './components/Login'
import Register from './components/Register'
import PageContent from './components/PageContent'

const UserContext = React.createContext({
  loggedIn: false,
  name: "",
  onLogout: () => true,
});

export const UserConsumer = UserContext.Consumer;
const UserProvider = UserContext.Provider;

export default class App extends Component{
  constructor(props){
    super(props)
    this.state = {};

    this.handleLogout = this.handleLogout.bind(this)
  };
  handleLogout(){
    console.log("Handling logout")
  }
  render(){
    return(
      <BrowserRouter history={hashHistory}>
        <UserProvider value={this.state.loggedIn, this.state.name, {onLogout: this.handleLogout}}>
          <div>
          <Route component={Banner} />
          {/*
          <Route path='/' component={Home} />
          <Route path='/' render={(props) => <Home text="Test" {...props} />} />
          */}

          <PageContent path='/' component={PageContent}>
            <Route exact path='/' component={Clock} />
            <Route path='/login' component={Login} />
            <Route path='/Register' component={Register} />
          </PageContent>
         </div>
        </UserProvider>
      </BrowserRouter>
    )
  }
};
