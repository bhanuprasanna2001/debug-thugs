import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './ReflectionForm.css';
import ProgressTracker from './progresstracker';

const ReflectionForm = () => {
  const [userId, setUserId] = useState(localStorage.getItem('user_id') || '');
  const [day, setDay] = useState('');
  const [plan, setPlan] = useState(null);
  const [likedSkills, setLikedSkills] = useState([]);
  const [dislikedSkills, setDislikedSkills] = useState([]);
  const [comments, setComments] = useState({});
  const [extraAnswers, setExtraAnswers] = useState({});
  const [days, setDays] = useState([1, 2]);
  

  useEffect(() => {
    if (!userId) {
      const newId = crypto.randomUUID();
      localStorage.setItem('user_id', newId);
      setUserId(newId);
    }
  }, [userId]);

  const fetchPlan = async (selectedDay) => {
    try {
      const res = await axios.get(`http://localhost:5000/api/bootcamp-day/${selectedDay}`);
      setPlan(res.data);
    } catch (err) {
      alert('Error fetching bootcamp plan.');
    }
  };

  const handleSkillSelection = (skill, list, setList) => {
    if (list.includes(skill)) {
      setList(list.filter(s => s !== skill));
    } else {
      setList([...list, skill]);
    }
  };

  const handleCommentChange = (skill, value) => {
    setComments(prev => ({ ...prev, [skill]: value }));
  };

  const handleExtraAnswer = (question, answer) => {
    setExtraAnswers(prev => ({ ...prev, [question]: answer }));
  };

  const handleSubmit = async () => {
    const payload = {
      user_id: userId,
      course_id: "lewagon_bootcamp",
      day,
      topic: plan.topic,
      module: plan.module,
      skills: plan.skills,
      liked_skills: likedSkills,
      disliked_skills: dislikedSkills,
      comments,
      extra_answers: extraAnswers
    };

    try {
      await axios.post("http://localhost:5000/api/save-reflection", payload);
      alert('✅ Reflection saved!');
      setPlan(null);
      setLikedSkills([]);
      setDislikedSkills([]);
      setComments({});
      setExtraAnswers({});
    } catch (err) {
      alert('❌ Failed to save reflection.');
    }
  };

  return (
    <div className="container reflection-form-container">
      <div className="reflection-motivation">
  💡 Reflecting helps turn experience into insight. Keep it up! 
  <span className="typing-dots" />
</div>
      <div className="reflection-banner my-4 p-4 shadow-sm rounded">
      <h5 className="text-success mb-2">✅ Great job completing Day {day}!</h5>
      <p className="mb-0">Let’s take a moment to reflect on what you learned and how you felt.</p>
    </div>
    {userId && <ProgressTracker userId={userId} />}
      <div className="card shadow-sm p-4 reflection-card">
        <h2 className="text-center text-primary mb-4">📝 Daily Reflection</h2>

        <div className="mb-3">
          <label className="form-label">Select Day:</label>
          <select value={day} onChange={e => { setDay(e.target.value); fetchPlan(e.target.value); }} className="form-select">
            <option value="">-- Select Day --</option>
            {days.map(d => <option key={d} value={d}>{`Day ${d}`}</option>)}
          </select>
        </div>

        {plan && (
          <div className="mt-4">
            <div className="mb-4">
              <h4 className="text-dark">📚 {plan.topic} <span className="text-muted">({plan.module})</span></h4>
              <p className="fw-bold">Skills covered:</p>
              <div className="">
                {plan.skills.map(skill => (
                  <span key={skill} className="badge bg-light text-dark border shadow-sm">{skill}</span>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <p className="section-title text-success">👍 Liked Skills</p>
              {plan.skills.map(skill => (
                <div key={skill} className="form-check mb-3">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    checked={likedSkills.includes(skill)}
                    onChange={() => handleSkillSelection(skill, likedSkills, setLikedSkills)}
                    id={`like-${skill}`}
                  />
                  <label className="form-check-label" htmlFor={`like-${skill}`}>{skill}</label>
                  {likedSkills.includes(skill) && (
                    <textarea
                      className="form-control mt-2"
                      placeholder="Why did you like this?"
                      value={comments[skill] || ''}
                      onChange={(e) => handleCommentChange(skill, e.target.value)}
                    />
                  )}
                </div>
              ))}
            </div>

            <div className="mb-4">
              <p className="section-title text-danger">👎 Disliked Skills</p>
              {plan.skills.map(skill => (
                <div key={skill} className="form-check mb-3">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    checked={dislikedSkills.includes(skill)}
                    onChange={() => handleSkillSelection(skill, dislikedSkills, setDislikedSkills)}
                    id={`dislike-${skill}`}
                  />
                  <label className="form-check-label" htmlFor={`dislike-${skill}`}>{skill}</label>
                  {dislikedSkills.includes(skill) && (
                    <textarea
                      className="form-control mt-2"
                      placeholder="Why didn’t you enjoy this?"
                      value={comments[skill] || ''}
                      onChange={(e) => handleCommentChange(skill, e.target.value)}
                    />
                  )}
                </div>
              ))}
            </div>

            {plan.questions && (
              <div className="mb-4">
                <p className="section-title text-primary">📋 Extra Questions</p>
                {plan.questions.map(q => (
                  <div key={q.question} className="mb-3">
                    <label className="form-label fw-medium">{q.question}</label>
                    <select
                      className="form-select"
                      value={extraAnswers[q.question] || ''}
                      onChange={(e) => handleExtraAnswer(q.question, e.target.value)}
                    >
                      <option value="">-- Choose an option --</option>
                      {q.options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                    </select>
                  </div>
                ))}
              </div>
            )}

            <div className="text-end">
              <button onClick={handleSubmit} className="btn btn-outline-primary">Submit Reflection</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReflectionForm;