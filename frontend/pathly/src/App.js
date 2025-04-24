import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ReflectionForm from './pages/components/form/reflectionform';
import LLMSummary from './pages/components/LLM/llmfrontend';
import ResumeJobRecommender from './pages/components/recommend/recommendation';

function App() {
  return (
    <Router>
      <div className="container py-4">
        <nav className="mb-4">
          <Link to="/" className="btn btn-outline-primary me-2 ms-2">📝 Reflect</Link>
          <Link to="/summary" className="btn btn-outline-primary">🧠 Summary</Link>
          <Link to="/jobsuggestion" className="btn btn-outline-primary ms-2">📄 Job Recommendation</Link>
        </nav>

        <Routes>
          <Route path="/" element={<ReflectionForm />} />
          <Route path="/summary" element={<LLMSummary />} />
          <Route path="/jobsuggestion" element={<ResumeJobRecommender />} />

        </Routes>
      </div>
    </Router>
  );
}

export default App;
