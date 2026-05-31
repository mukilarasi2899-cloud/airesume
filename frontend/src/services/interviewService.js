import api from './api';

export const interviewService = {
  // Start new interview
  startInterview: async (jobRole, numTechnical = 5, numHr = 3, userId = null) => {
    const response = await api.post('/interview/start', {
      job_role: jobRole,
      num_technical: numTechnical,
      num_hr: numHr,
      user_id: userId,
    });
    return response.data;
  },

  // Submit answer
  submitAnswer: async (interviewId, questionId, answerText, timeTaken = null) => {
    const response = await api.post(`/interview/${interviewId}/answer`, {
      question_id: questionId,
      answer_text: answerText,
      time_taken_seconds: timeTaken,
    });
    return response.data;
  },

  // Complete interview
  completeInterview: async (interviewId) => {
    const response = await api.post(`/interview/${interviewId}/complete`);
    return response.data;
  },

  // Get interview details
  getInterview: async (interviewId) => {
    const response = await api.get(`/interview/${interviewId}`);
    return response.data;
  },

  // Get user's interviews
  getUserInterviews: async (userId, limit = 10, skip = 0) => {
    const response = await api.get(`/interview/user/${userId}`, {
      params: { limit, skip },
    });
    return response.data;
  },

  // Get available roles
  getAvailableRoles: async () => {
    const response = await api.get('/interview/roles/available');
    return response.data;
  },

  // Get interview statistics
  getInterviewStats: async (interviewId) => {
    const response = await api.get(`/interview/stats/${interviewId}`);
    return response.data;
  },
};
