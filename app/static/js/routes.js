import React from 'react';
import { HashRouter, Route, hashHistory } from 'react-router-dom';
import Home from './components/Home';
import Clock from './components/Clock'
import Banner from './components/Banner'
import Login from './components/Login'
import Register from './components/Register'
import PageContent from './components/PageContent'
// import more components
export default (
    <HashRouter history={hashHistory}>
     <div>
      <Route component={Banner} />

      <Route path='/' component={Home} />
      <Route path='/' render={(props) => <Home text="Test" {...props} />} />


      <PageContent path='/' component={PageContent}>
        <Route exact path='/' component={Clock} />
        <Route path='/login' component={Login} />
        <Route path='/Register' component={Register} />
      </PageContent>



     </div>
    </HashRouter>
);
