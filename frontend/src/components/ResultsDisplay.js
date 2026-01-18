import React from 'react';
import './ResultsDisplay.css';

function ResultsDisplay({ result }) {
  if (!result) return null;

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'PASS': return '#48bb78';
      case 'REVIEW': return '#ed8936';
      case 'FAIL': return '#f56565';
      default: return '#718096';
    }
  };

  const getRecommendationIcon = (recommendation) => {
    switch (recommendation) {
      case 'PASS': return '✅';
      case 'REVIEW': return '⚠️';
      case 'FAIL': return '❌';
      default: return '📊';
    }
  };

  return (
    <div className="results-container">
      <h2>🎯 Screening Results</h2>
      
      <div className="result-card">
        <h3>Candidate Information</h3>
        <div className="info-row">
          <span className="label">Name:</span>
          <span className="value">{result.candidate_name}</span>
        </div>
        <div className="info-row">
          <span className="label">File:</span>
          <span className="value">{result.file_name}</span>
        </div>
      </div>

      <div className="result-card">
        <h3>Match Score</h3>
        <div className="score-display">
          <div className="score-circle">
            <span className="score-number">{result.match_score}%</span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${result.match_score}%` }}
            ></div>
          </div>
        </div>
      </div>

      <div
        className="result-card recommendation-card"
        style={{ borderColor: getRecommendationColor(result.recommendation) }}
      >
        <h3>Recommendation</h3>
        <div
          className="recommendation-badge"
          style={{ backgroundColor: getRecommendationColor(result.recommendation) }}
        >
          {getRecommendationIcon(result.recommendation)} {result.recommendation}
        </div>
      </div>

      <div className="result-card">
        <h3>Skills Analysis</h3>
        
        <div className="skills-section">
          <h4 className="matched-title">✅ Matched Skills</h4>
          <div className="skills-list">
            {result.matched_skills && result.matched_skills.length > 0 ? (
              result.matched_skills.map((skill, index) => (
                <span key={index} className="skill-tag matched">{skill}</span>
              ))
            ) : (
              <p className="no-skills">No matched skills</p>
            )}
          </div>
        </div>

        <div className="skills-section">
          <h4 className="missing-title">❌ Missing Skills</h4>
          <div className="skills-list">
            {result.missing_skills && result.missing_skills.length > 0 ? (
              result.missing_skills.map((skill, index) => (
                <span key={index} className="skill-tag missing">{skill}</span>
              ))
            ) : (
              <p className="no-skills">No missing skills</p>
            )}
          </div>
        </div>
      </div>

      {result.ai_powered && (
        <div className="ai-badge">
          🤖 Powered by AI Semantic Matching
        </div>
      )}
    </div>
  );
}

export default ResultsDisplay;
