import React, { useState } from 'react';
import './ResultsTable.css';

function ResultsTable({ batchResults }) {
  const [sortBy, setSortBy] = useState('match_score');
  const [sortOrder, setSortOrder] = useState('desc');

  if (!batchResults || !batchResults.results || batchResults.results.length === 0) {
    return null;
  }

  const results = batchResults.results;

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
  };

  const sortedResults = [...results].sort((a, b) => {
    let aValue = a[sortBy];
    let bValue = b[sortBy];
    
    if (sortBy === 'match_score') {
      aValue = parseFloat(aValue) || 0;
      bValue = parseFloat(bValue) || 0;
    }
    
    if (sortOrder === 'asc') {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  const getRecommendationClass = (recommendation) => {
    switch (recommendation) {
      case 'PASS': return 'badge-pass';
      case 'REVIEW': return 'badge-review';
      case 'FAIL': return 'badge-fail';
      default: return 'badge-error';
    }
  };

  const getRecommendationIcon = (recommendation) => {
    switch (recommendation) {
      case 'PASS': return '✅';
      case 'REVIEW': return '⚠️';
      case 'FAIL': return '❌';
      default: return '⚠️';
    }
  };

  const exportToCSV = () => {
    const headers = ['Candidate Name', 'File Name', 'Match Score', 'Recommendation', 'Matched Skills', 'Missing Skills'];
    const rows = results.map(r => [
      r.candidate_name,
      r.file_name,
      r.match_score,
      r.recommendation,
      r.matched_skills ? r.matched_skills.join(', ') : '',
      r.missing_skills ? r.missing_skills.join(', ') : ''
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `screening_results_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
  };

  return (
    <div className="results-table-container">
      <div className="results-header">
        <h2>📊 Screening Results</h2>
        <div className="results-actions">
          <span className="results-count">Total: {results.length} candidate(s)</span>
          <button className="export-btn" onClick={exportToCSV}>
            💾 Export CSV
          </button>
        </div>
      </div>

      <div className="table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('candidate_name')}>
                Candidate {sortBy === 'candidate_name' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('file_name')}>
                File {sortBy === 'file_name' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('match_score')}>
                Score {sortBy === 'match_score' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('recommendation')}>
                Recommendation {sortBy === 'recommendation' && (sortOrder === 'asc' ? '↑' : '↓')}
              </th>
              <th>Matched Skills</th>
              <th>Missing Skills</th>
            </tr>
          </thead>
          <tbody>
            {sortedResults.map((result, index) => (
              <tr key={index}>
                <td className="candidate-name">{result.candidate_name}</td>
                <td className="file-name">{result.file_name}</td>
                <td className="match-score">
                  <div className="score-cell">
                    <div className="score-bar" style={{ width: `${result.match_score}%` }}></div>
                    <span className="score-text">{result.match_score}%</span>
                  </div>
                </td>
                <td className="recommendation">
                  <span className={`badge ${getRecommendationClass(result.recommendation)}`}>
                    {getRecommendationIcon(result.recommendation)} {result.recommendation}
                  </span>
                </td>
                <td className="skills">
                  {result.matched_skills && result.matched_skills.length > 0 ? (
                    <div className="skills-tags">
                      {result.matched_skills.slice(0, 3).map((skill, i) => (
                        <span key={i} className="skill-tag matched">{skill}</span>
                      ))}
                      {result.matched_skills.length > 3 && (
                        <span className="more-skills">+{result.matched_skills.length - 3}</span>
                      )}
                    </div>
                  ) : (
                    <span className="no-skills">None</span>
                  )}
                </td>
                <td className="skills">
                  {result.missing_skills && result.missing_skills.length > 0 ? (
                    <div className="skills-tags">
                      {result.missing_skills.slice(0, 3).map((skill, i) => (
                        <span key={i} className="skill-tag missing">{skill}</span>
                      ))}
                      {result.missing_skills.length > 3 && (
                        <span className="more-skills">+{result.missing_skills.length - 3}</span>
                      )}
                    </div>
                  ) : (
                    <span className="no-skills">None</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {batchResults.ai_powered && (
        <div className="ai-badge">
          🤖 Powered by AI Semantic Matching
        </div>
      )}
    </div>
  );
}

export default ResultsTable;
