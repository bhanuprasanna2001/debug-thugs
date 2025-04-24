import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const LLMSummary = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get('http://localhost:5000/api/llm-summary');
      setSummary(res.data);
    } catch (err) {
      setError("Failed to generate summary.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="text-center mb-4">
        <h2 className="text-primary">🧠 Weekly Career Insight</h2>
        <p className="text-muted">Get personalized strengths, challenges, and career guidance from your reflections.</p>
        <button className="btn btn-outline-primary mt-3" onClick={handleGenerateSummary} disabled={loading}>
          {loading ? 'Thinking...' : 'Generate Weekly Summary'}
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {summary && (
        <div className="card shadow-sm p-4">
            <h3 className="text-muted mb-3">
      🆔 <strong>User ID:</strong> <code>{summary.user_id}</code>
    </h3>
          <h4>✨ Strengths</h4>
          <ul>{summary.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul>

          <h4 className="mt-4">⚠️ Challenges</h4>
          <ul>{summary.challenges.map((c, i) => <li key={i}>{c}</li>)}</ul>

          <h4 className="mt-4">🎯 Weekly Recommendations</h4>
          <ul>{summary.weekly_recommendations.map((r, i) => <li key={i}>{r}</li>)}</ul>

          <h4 className="mt-4">🚀 Career Path Suggestions</h4>
          <ul>
            {summary.potential_career_paths.map((p, i) => (
              <li key={i}><strong>{p.title}:</strong> {p.reason}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LLMSummary;
