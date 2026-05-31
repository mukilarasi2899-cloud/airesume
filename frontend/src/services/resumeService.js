import api from './api';

export const resumeService = {
  // Upload and analyze resume
  uploadResume: async (file, jobRole = null, jobDescription = null, userId = null) => {
    const formData = new FormData();
    formData.append('file', file);
    if (jobRole) formData.append('job_role', jobRole);
    if (jobDescription) formData.append('job_description', jobDescription);
    if (userId) formData.append('user_id', userId);

    const response = await api.post('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get resume by ID
  getResume: async (resumeId) => {
    const response = await api.get(`/resume/${resumeId}`);
    return response.data;
  },

  // Get user's resumes
  getUserResumes: async (userId, limit = 10, skip = 0) => {
    const response = await api.get(`/resume/user/${userId}`, {
      params: { limit, skip },
    });
    return response.data;
  },

  // Delete resume
  deleteResume: async (resumeId) => {
    const response = await api.delete(`/resume/${resumeId}`);
    return response.data;
  },
};
