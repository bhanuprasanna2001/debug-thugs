import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const ResumeJobRecommender = () => {
  const [resumeText, setResumeText] = useState('');
  const [predictedCategory, setPredictedCategory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!resumeText.trim()) return;
    setLoading(true);
    setError(null);
    setPredictedCategory(null);

    try {
      const response = await axios.post('http://localhost:5000/api/job-recommendation', { resume_text: resumeText });
      setPredictedCategory(response.data.predicted_category);
    } catch (err) {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-primary">📄 Resume Job Recommender</h2>
      <p className="text-muted">Paste your resume text below and get a predicted job category based on it.</p>

      <textarea
        className="form-control mb-3"
        rows={10}
        placeholder="Paste your resume here..."
        value={resumeText}
        onChange={(e) => setResumeText(e.target.value)}
      ></textarea>

      <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
        {loading ? 'Analyzing...' : 'Get Recommendation'}
      </button>

      {error && <div className="alert alert-danger mt-3">{error}</div>}
      {predictedCategory && (
        <div className="alert alert-success mt-3">
          🎯 <strong>Recommended Job Category:</strong> {predictedCategory}
        </div>
      )}
    </div>
  );
};

export default ResumeJobRecommender;