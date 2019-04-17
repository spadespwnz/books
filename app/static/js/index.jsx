import React from 'react';
import ReactDOM from 'react-dom';
import App from "./App";
import { BrowserRouter,  browserHistory,  } from 'react-router-dom';
ReactDOM.render(
        <BrowserRouter history={browserHistory}>
          <App />
        </BrowserRouter>
        , document.getElementById("content"));
