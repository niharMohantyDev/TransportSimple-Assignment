import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router';
import './UserQuestions.css';

const UserQuestions = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [answersLoading, setAnswersLoading] = useState(false);
  const [archiveLoading, setArchiveLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          navigate('/login');
          return;
        }

        const response = await axios.get('http://127.0.0.1:8000/api/get-my-questions', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (response.data.Status === 'Success') {
          setQuestions(response.data.Data);
          if (response.data.accessToken) {
            localStorage.setItem('accessToken', response.data.accessToken);
          }
        }
      } catch (err) {
        setError('Failed to fetch questions');
        if (err.response && (err.response.status === 401 || err.response.status === 403)) {
          localStorage.removeItem('accessToken');
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [navigate]);

  const fetchAnswers = async (questionId) => {
    try {
      setAnswersLoading(true);
      setError('');
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/login');
        return;
      }

      const response = await axios.post(
        'http://localhost:8000/api/get-answer',
        { questionId },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.Status === 'Success') {
        setAnswers(response.data.Data);
        if (response.data.accessToken) {
          localStorage.setItem('accessToken', response.data.accessToken);
        }
      }
    } catch (err) {
      setError('Failed to fetch answers');
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        localStorage.removeItem('accessToken');
        navigate('/login');
      }
    } finally {
      setAnswersLoading(false);
    }
  };

  const handleQuestionClick = (question) => {
    if (selectedQuestion?.id === question.id) {
      setSelectedQuestion(null);
      setAnswers([]);
    } else {
      setSelectedQuestion(question);
      fetchAnswers(question.id);
    }
  };

  const archiveQuestion = async (questionId) => {
    try {
      setArchiveLoading(true);
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/login');
        return;
      }

      const response = await axios.post(
        'http://localhost:8000/api/archive-question',
        { questionId },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.Status === 'Success') {
        // Refresh the questions list
        const updatedQuestions = questions.map(q => 
          q.id === questionId ? { ...q, isActive: false } : q
        );
        setQuestions(updatedQuestions);
        
        if (response.data.accessToken) {
          localStorage.setItem('accessToken', response.data.accessToken);
        }
      }
    } catch (err) {
      setError('Failed to archive question');
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        localStorage.removeItem('accessToken');
        navigate('/login');
      }
    } finally {
      setArchiveLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading your questions...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="user-questions-container">
      <h2>Questions You Asked</h2>
      {questions.length === 0 ? (
        <p>You haven't asked any questions yet.</p>
      ) : (
        <div className="questions-list">
          {questions.map((question) => (
            <div key={question.id} className="user-question-card">
              <div 
                className={`question-header ${selectedQuestion?.id === question.id ? 'selected' : ''}`}
                onClick={() => handleQuestionClick(question)}
              >
                <span className="question-id">#{question.id}</span>
                <span className={`question-status ${question.isActive ? 'active' : 'inactive'}`}>
                  {question.isActive ? 'Active' : 'Archived'}
                </span>
              </div>
              <div className="question-content">
                <p>{question.question}</p>
              </div>
              <div className="question-footer">
                <span className="question-username">Asked by: {question.username}</span>
                {question.isActive && (
                  <button 
                    className="archive-button"
                    onClick={(e) => {
                      e.stopPropagation();
                      archiveQuestion(question.id);
                    }}
                    disabled={archiveLoading}
                  >
                    {archiveLoading ? 'Archiving...' : 'Archive'}
                  </button>
                )}
              </div>
              
              {selectedQuestion?.id === question.id && (
                <div className="answers-section">
                  <h3>Answers ({answers.length})</h3>
                  {answersLoading ? (
                    <div className="loading">Loading answers...</div>
                  ) : answers.length > 0 ? (
                    <div className="answers-list">
                      {answers.map((answer) => (
                        <div key={answer.id} className="answer-card">
                          <div className="answer-content">
                            <p>{answer.answer}</p>
                          </div>
                          <div className="answer-footer">
                            <span className="answer-username">Answered by: {answer.username}</span>
                            <div className="answer-votes">
                              <span className="likes">Likes: {answer.likes || 0}</span>
                              <span className="dislikes">Dislikes: {answer.dislikes || 0}</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p>No answers yet for this question.</p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UserQuestions;