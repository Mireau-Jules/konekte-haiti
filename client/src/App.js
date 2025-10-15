import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import ServiceList from './components/ServiceList';
import ServiceDetail from './components/ServiceDetail';
import AddServiceForm from './components/AddServiceForm';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <div className="container">
          <Routes>
            <Route path="/" element={<ServiceList />} />
            <Route path="/services/:id" element={<ServiceDetail />} />
            <Route path="/add-service" element={<AddServiceForm />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;