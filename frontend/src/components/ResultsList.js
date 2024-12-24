import React from "react";

function ResultsList({ results }) {
  return (
    <div className="results-list">
      {results.map((paper, index) => (
        <div className="result-item" key={index}>
          <h3>{paper.title}</h3>
          <p>
            <strong>Authors:</strong> {paper.authors.join(", ")}
          </p>
          <p>{paper.abstract}</p>
          <a href={paper.url} target="_blank" rel="noopener noreferrer">
            Read More
          </a>
        </div>
      ))}
    </div>
  );
}

export default ResultsList;