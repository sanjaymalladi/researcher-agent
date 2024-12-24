import React, { useState } from "react";

function SearchBar({ onSearch }) {
  const [topic, setTopic] = useState("");

  const handleSearch = () => {
    onSearch(topic);
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Enter a research topic"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}

export default SearchBar;