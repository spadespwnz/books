import React from 'react';
import { HashRouter, Route, hashHistory } from 'react-router-dom';
import Home from './components/Home';
import Clock from './components/Clock'
import Banner from './components/Banner'
// import more components
export default (
    <HashRouter history={hashHistory}>
     <div>
      <Route component={Banner} />
      <Route path='/' component={Home} />
      <Route path='/' render={(props) => <Home text="Test" {...props} />} />
      <Route path='/' component={Clock} />
     </div>
    </HashRouter>
);
