// import axios from 'axios';

// const API_BASE_URL = 'http://localhost:8001';

// const api = axios.create({
//   baseURL: API_BASE_URL,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

// // Add token to requests
// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem('token');
//   const hrToken = localStorage.getItem('hrToken');
  
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   } else if (hrToken) {
//     config.headers.Authorization = `Bearer ${hrToken}`;
//   }
//   return config;
// });

// // Auth APIs
// export const register = async (userData) => {
//   const response = await api.post('/auth/register', userData);
//   return response.data;
// };

// export const login = async (credentials) => {
//   const response = await api.post('/auth/login', credentials);
//   return response.data;
// };

// export const getCurrentUser = async () => {
//   const response = await api.get('/auth/me');
//   return response.data;
// };

// // HR APIs
// export const registerCompany = async (companyData) => {
//   const response = await api.post('/hr/register', companyData);
//   return response.data;
// };

// export const loginCompany = async (credentials) => {
//   const response = await api.post('/hr/login', credentials);
//   return response.data;
// };

// export const getCurrentCompany = async () => {
//   const response = await api.get('/hr/me');
//   return response.data;
// };

// // export const getCompanyApplications = async (statusFilter = null) => {
// //   const params = statusFilter ? { status_filter: statusFilter } : {};
// //   const response = await api.get('/hr/applications', { params });
// //   return response.data;
// // };

// export const updateApplicationStatus = async (applicationId, newStatus) => {
//   const response = await api.patch(`/hr/applications/${applicationId}/status`, null, {
//     params: { new_status: newStatus }
//   });
//   return response.data;
// };

// // Resume APIs
// export const uploadResume = async (file) => {
//   const formData = new FormData();
//   formData.append('file', file);
  
//   const response = await api.post('/resume/upload', formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data',
//     },
//   });
//   return response.data;
// };

// export const getMyResumes = async () => {
//   const response = await api.get('/resume/my-resumes');
//   return response.data;
// };

// export const getJobRecommendations = async (resumeId, topN = 10) => {
//   const response = await api.get('/jobs/recommendations', {
//     params: {
//       resume_id: resumeId,
//       top_n: topN
//     }
//   });

//   return response.data;
// };




// // Application APIs
// export const applyToJob = async (applicationData) => {
//   const response = await api.post('/applications/apply', applicationData);
//   return response.data;
// };

// export const getMyApplications = async () => {
//   const response = await api.get('/applications/my-applications');
//   return response.data;
// };

// export const checkApplicationStatus = async (jobId) => {
//   const response = await api.get(`/applications/check/${jobId}`);
//   return response.data;
// };


// // Resume viewing for HR
// export const viewResumeDetails = async (resumeId) => {
//   const response = await api.get(`/applications/view-resume/${resumeId}`);
//   return response.data;
// };

// export const downloadResume = async (resumeId, filename) => {
//   const response = await api.get(`/applications/download-resume/${resumeId}`, {
//     responseType: 'blob'
//   });
  
//   // Create download link
//   const url = window.URL.createObjectURL(new Blob([response.data]));
//   const link = document.createElement('a');
//   link.href = url;
//   link.setAttribute('download', filename);
//   document.body.appendChild(link);
//   link.click();
//   link.remove();
  
//   return response.data;
// };


// // Add these new exports to your existing api.js

// // HR Job Management
// export const createJob = async (jobData) => {
//   const response = await api.post('/hr/jobs', jobData);
//   return response.data;
// };

// export const updateJob = async (jobId, jobData) => {
//   const response = await api.put(`/hr/jobs/${jobId}`, jobData);
//   return response.data;
// };

// export const deleteJob = async (jobId) => {
//   const response = await api.delete(`/hr/jobs/${jobId}`);
//   return response.data;
// };

// export const getHRJobs = async () => {
//   const response = await api.get('/hr/jobs');
//   return response.data;
// };

// // Updated getCompanyApplications with search support
// export const getCompanyApplications = async (statusFilter = null, search = null) => {
//   const params = {};
//   if (statusFilter) params.status_filter = statusFilter;
//   if (search) params.search = search;
//   const response = await api.get('/hr/applications', { params });
//   return response.data;
// };


// export default api;




import axios from 'axios';

// Dynamic API URL based on environment
const getApiBaseUrl = () => {
  // Production: Use Render backend URL
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // Development: Use localhost
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:8001';
  }
  
  // Fallback
  return 'http://localhost:8001';
};

const API_BASE_URL = getApiBaseUrl();

console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout for production
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const hrToken = localStorage.getItem('hrToken');
    const userToken = localStorage.getItem('token');
    const token = hrToken || userToken;
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log('API Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.config?.url);
    
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('hrToken');
      
      // Only redirect if not already on login page
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;

// Export base URL for debugging
export const getApiUrl = () => API_BASE_URL;

// ============================================
// AUTH APIs
// ============================================

export const register = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

export const login = async (credentials) => {
  const response = await api.post('/auth/login', credentials);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// ============================================
// HR APIs
// ============================================

export const registerCompany = async (companyData) => {
  const response = await api.post('/hr/register', companyData);
  return response.data;
};

export const loginCompany = async (credentials) => {
  const response = await api.post('/hr/login', credentials);
  return response.data;
};

export const getCurrentCompany = async () => {
  const response = await api.get('/hr/me');
  return response.data;
};

export const getCompanyApplications = async (statusFilter = null, search = null) => {
  const params = {};
  if (statusFilter) params.status_filter = statusFilter;
  if (search) params.search = search;
  const response = await api.get('/hr/applications', { params });
  return response.data;
};

export const updateApplicationStatus = async (applicationId, newStatus) => {
  const response = await api.patch(`/hr/applications/${applicationId}/status`, null, {
    params: { new_status: newStatus }
  });
  return response.data;
};

export const createJob = async (jobData) => {
  const response = await api.post('/hr/jobs', jobData);
  return response.data;
};

export const getHRJobs = async () => {
  const response = await api.get('/hr/jobs');
  return response.data;
};

export const updateJob = async (jobId, jobData) => {
  const response = await api.put(`/hr/jobs/${jobId}`, jobData);
  return response.data;
};

export const deleteJob = async (jobId) => {
  const response = await api.delete(`/hr/jobs/${jobId}`);
  return response.data;
};

// ============================================
// RESUME APIs
// ============================================

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/resume/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getMyResumes = async () => {
  const response = await api.get('/resume/my-resumes');
  return response.data;
};

export const deleteResume = async (resumeId) => {
  const response = await api.delete(`/resume/${resumeId}`);
  return response.data;
};

// ============================================
// JOBS APIs
// ============================================

export const getJobRecommendations = async (resumeId, topN = 10) => {
  const response = await api.get('/jobs/recommendations', {
    params: { resume_id: resumeId, top_n: topN }
  });
  return response.data;
};

// ============================================
// APPLICATIONS APIs
// ============================================

export const applyToJob = async (applicationData) => {
  const response = await api.post('/applications/apply', applicationData);
  return response.data;
};

export const getMyApplications = async () => {
  const response = await api.get('/applications/my-applications');
  return response.data;
};

export const checkApplicationStatus = async (jobId) => {
  const response = await api.get(`/applications/check/${jobId}`);
  return response.data;
};

export const viewResumeDetails = async (resumeId) => {
  const response = await api.get(`/applications/view-resume/${resumeId}`);
  return response.data;
};

export const downloadResume = async (resumeId, filename) => {
  const response = await api.get(`/applications/download-resume/${resumeId}`, {
    responseType: 'blob'
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  
  return response.data;
};