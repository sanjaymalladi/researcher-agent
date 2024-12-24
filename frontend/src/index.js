import React from 'react';
import ReactDOM from 'react-dom/client';
import 'styles/App.css';  // Global styles (you can customize it)
import App from './App'; // Main App component
import { BrowserRouter as Router } from 'react-router-dom'; // For routing if needed

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);

// Rendering the App component inside the root div
root.render(
  <React.StrictMode>
    <Router>  {/* Optional if you're using routing */}
      <App />
    </Router>
  </React.StrictMode>
);
