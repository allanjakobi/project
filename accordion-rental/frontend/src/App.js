// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import AccordionList from './components/AccordionList';
import Register from './components/Register';
import AdminDashboard from './components/AdminDashboard';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={AccordionList} />
        <Route path="/register" component={Register} />
        <Route path="/admin" component={AdminDashboard} />
        {/* Add more routes as needed */}
      </Switch>
    </Router>
  );
}

export default App;
