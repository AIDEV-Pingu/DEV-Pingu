import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import MainPage from './MainPage';
import './App.css';

class App extends React.Component {
  render() {
    return (
      <Router>
        <MainPage />
      </Router>
    );
  }
}

export default App;