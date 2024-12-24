import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";
import "./styles/App.css";

function App() {
  const [results, setResults] = useState([]);

  const handleSearch = async (topic) => {
    const response = await fetch("http://localhost:5000/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, limit: 10 }),
    });
    const data = await response.json();
    setResults(data.papers || []);
  };

  return (
    <div className="app">
      <h1>Researcher Agent</h1>
      <SearchBar onSearch={handleSearch} />
      <ResultsList results={results} />
    </div>
  );
}

export default App;