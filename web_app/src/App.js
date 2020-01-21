import React, { Component } from 'react';
import {BrowserRouter, Route} from 'react-router-dom';
import Home from './Views/Home';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div>
        <Route exact = {true} path = '/' render = {() => (
          <div className = "App">
            <Home />
          </div>
        )}/>
      </div>
    </BrowserRouter>
  );
}

export default App;
