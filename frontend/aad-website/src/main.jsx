import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';

import Login from './Login.jsx';
import Dashboard from './Dashboard.jsx';


createRoot(document.getElementById('root')).render(
  <StrictMode>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} /> 
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
  </StrictMode>,

);

