import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Global styles (make sure index.css exists)
import App from './App.jsx'; // Main App component

// This will render the App component inside the 'root' div in public/index.html
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')  // Make sure there's an element with id='root' in index.html
);
