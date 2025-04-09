import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router";
import "./Dashboard.css";
import Logout from './Logout';
import UserQuestions from './UserQuestions';
import axios from 'axios';

const Dashboard = () => {
  const [showQuestions, setShowQuestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [allQuestions, setAllQuestions] = useState([]);
  const [allQuestionsLoading, setAllQuestionsLoading] = useState(true);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [answersLoading, setAnswersLoading] = useState(false);
  const [answerText, setAnswerText] = useState('');
  const [isAnswering, setIsAnswering] = useState(false);
  const navigate = useNavigate();

  // Reusable fetch function for all questions
  const fetchAllQuestions = useCallback(async () => {
    try {
      setAllQuestionsLoading(true);
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/login');
        return;
      }

      const response = await axios.get(
        'http://localhost:8000/api/get-all-questions',
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          }
        }
      );
      if (response.data.Status === 'Success') {
        setAllQuestions(response.data.Data);
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
      setAllQuestionsLoading(false);
    }
  }, [navigate]);

  // Fetch answers for a question
  const fetchAnswers = useCallback(async (questionId) => {
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
  }, [navigate]);

  // Handle question click
  const handleQuestionClick = (question) => {
    setSelectedQuestion(question);
    fetchAnswers(question.id);
  };

  // Handle like/dislike
  const handleVote = async (answerId, action) => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/login');
        return;
      }

      // Prepare the request based on the action
      const requestData = {
        answerId,
        like: action === 'like' ? "True" : "False",
        dislike: action === 'dislike' ? "True" : "False"
      };

      const response = await axios.post(
        'http://localhost:8000/api/likes-dislikes',
        requestData,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.accessToken) {
        localStorage.setItem('accessToken', response.data.accessToken);
      }

      if (response.data.Status === 'Success') {
        setSuccess(`Answer ${action}d successfully!`);
        // Refresh answers after voting
        if (selectedQuestion) {
          await fetchAnswers(selectedQuestion.id);
        }
      } else {
        setError(response.data.Message || `Failed to ${action} answer`);
      }
    } catch (err) {
      if (err.response) {
        if (err.response.status === 401 || err.response.status === 403) {
          localStorage.removeItem('accessToken');
          navigate('/login');
        } else {
          setError(err.response.data?.Message || `Failed to ${action} answer`);
        }
      } else {
        setError('Network error. Please try again.');
      }
    }
  };

  // Post an answer
  const postAnswer = async () => {
    if (!answerText.trim()) {
      setError('Answer cannot be empty');
      return;
    }

    try {
      setIsAnswering(true);
      setError('');
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/login');
        return;
      }

      const response = await axios.post(
        'http://localhost:8000/api/post-answer',
        {
          answer: answerText,
          questionId: selectedQuestion.id
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.Status === 'Success') {
        setSuccess('Answer posted successfully!');
        setAnswerText('');
        if (response.data.accessToken) {
          localStorage.setItem('accessToken', response.data.accessToken);
        }
        // Refresh answers
        if (selectedQuestion) {
          await fetchAnswers(selectedQuestion.id);
        }
      }
    } catch (err) {
      setError(err.response?.data?.Message || 'Failed to post answer');
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        localStorage.removeItem('accessToken');
        navigate('/login');
      }
    } finally {
      setIsAnswering(false);
    }
  };

  // Initial fetch when component mounts
  useEffect(() => {
    fetchAllQuestions();
  }, [fetchAllQuestions]);

  const onAddQuestion = async () => {
    try {
      setLoading(true);
      setError('');
      setSuccess('');
      
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        navigate('/login');
        return;
      }

      const questionText = prompt('Enter your question:');
      if (!questionText) return;

      const response = await axios.post(
        'http://localhost:8000/api/post-question',
        { question: questionText },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.Status === 'Success') {
        setSuccess(response.data.Message);
        if (response.data.accessToken) {
          localStorage.setItem('accessToken', response.data.accessToken);
        }

        await fetchAllQuestions();

        if (showQuestions) {
          setShowQuestions(false);
          setTimeout(() => setShowQuestions(true), 100);
        }
      }
    } catch (err) {
      if (err.response) {
        if (err.response.status === 401 || err.response.status === 403) {
          localStorage.removeItem('accessToken');
          navigate('/login');
        } else {
          setError(err.response.data?.Message || 'Failed to post question');
        }
      } else {
        setError('Network error. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleQuestionsView = () => {
    setShowQuestions(!showQuestions);
    setError('');
    setSuccess('');
  };

  return (
    <div className="dashboard-container">
      <Logout />
      <br />
      
      {loading && <div className="loading-message">Posting question...</div>}
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="action-bar">
        <button 
          className="AddQuestionButton" 
          onClick={onAddQuestion}
          disabled={loading}
        >
          {loading ? 'Posting...' : 'Add New Question'}
        </button>
        <button 
          className="ViewQuestionsButton" 
          onClick={toggleQuestionsView}
          disabled={loading}
        >
          {showQuestions ? 'Hide My Questions' : 'Questions I Asked'}
        </button>
        <button
          className="RefreshButton"
          onClick={fetchAllQuestions}
          disabled={allQuestionsLoading}
        >
          {allQuestionsLoading ? 'Refreshing...' : 'Refresh Questions'}
        </button>
      </div>

      {showQuestions && <UserQuestions />}

      <h1 className="HeadingDash">Questions from everybody</h1>
      
      {allQuestionsLoading ? (
        <div className="loading-message">Loading all questions...</div>
      ) : (
        <div className="all-questions-container">
          {allQuestions.length > 0 ? (
            <div className="questions-grid">
              {allQuestions.map((question) => (
                <div 
                  key={question.id} 
                  className={`question-card ${selectedQuestion?.id === question.id ? 'selected' : ''}`}
                  onClick={() => handleQuestionClick(question)}
                >
                  <div className="question-header">
                    <span className="question-id">#{question.id}</span>
                    <span className="question-status">
                      {question.isActive ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <div className="question-content">
                    <p>{question.question}</p>
                  </div>
                  <div className="question-footer">
                    <span className="question-username">Asked by: {question.username}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No questions found.</p>
          )}
        </div>
      )}

      {/* Answers section */}
      {selectedQuestion && (
        <div className="answers-section">
          <h2>Answers for: "{selectedQuestion.question}"</h2>
          
          {/* Answer input form */}
          <div className="answer-form">
            <textarea
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              placeholder="Write your answer here..."
              rows={3}
            />
            <button 
              onClick={postAnswer}
              disabled={isAnswering || !answerText.trim()}
              className="post-answer-button"
            >
              {isAnswering ? 'Posting...' : 'Post Answer'}
            </button>
          </div>
          
          {answersLoading ? (
            <div className="loading-message">Loading answers...</div>
          ) : answers.length > 0 ? (
            <div className="answers-grid">
              {answers.map((answer) => (
                <div key={answer.id} className="answer-card">
                  <div className="answer-content">
                    <p>{answer.answer}</p>
                  </div>
                  <div className="answer-footer">
                    <span className="answer-username">Answered by: {answer.username}</span>
                    <div className="answer-votes">
                      <button 
                        className="like-button"
                        onClick={() => handleVote(answer.id, 'like')}
                      >
                        Like ({answer.likes})
                      </button>
                      <button 
                        className="dislike-button"
                        onClick={() => handleVote(answer.id, 'dislike')}
                      >
                        Dislike ({answer.dislikes})
                      </button>
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

      <div className="dashboard-footer">
        <p>Made with ❤️ by Nihar, ©️ all rights reserved</p>
      </div>
    </div>
  );
};

export default Dashboard;
