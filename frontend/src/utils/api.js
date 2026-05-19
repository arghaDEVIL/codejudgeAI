import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem("access_token");
            localStorage.removeItem("user");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    signup: (data) => api.post("/auth/signup/", data),
    login: (data) => api.post("/auth/login/", data),
    getCurrentUser: () => api.get("/auth/me/"),
};

// Problems API
export const problemsAPI = {
    getAll: (params = {}) => {
        const queryParams = new URLSearchParams();
        if (params.difficulty) queryParams.append('difficulty', params.difficulty);
        if (params.tags) queryParams.append('tags', params.tags);
        if (params.search) queryParams.append('search', params.search);
        if (params.page) queryParams.append('page', params.page.toString());
        if (params.limit) queryParams.append('limit', params.limit.toString());

        const queryString = queryParams.toString();
        return api.get(`/problems/${queryString ? `?${queryString}` : ''}`);
    },
    getById: (id) => api.get(`/problems/${id}/`),
    create: (data) => api.post("/problems/", data),
    getTags: () => api.get("/problems/tags"),
    getStats: () => api.get("/problems/stats"),
};

// Submissions API
export const submissionsAPI = {
    submit: (data) => api.post("/submissions/", data),
    getUserSubmissions: (params = {}) => {
        return api.get("/submissions/", { params });
    },
    getAll: () => api.get("/submissions/"),
    getById: (id) => api.get(`/submissions/${id}/`),
};

// Testcases API
export const testcasesAPI = {
    getByProblem: (problemId) => api.get(`/testcases/problem/${problemId}/`),
    create: (data) => api.post("/testcases/", data),
    update: (id, data) => api.put(`/testcases/${id}/`, data),
    delete: (id) => api.delete(`/testcases/${id}/`),
};

// AI Feedback API
export const aiFeedbackAPI = {
    getBySubmission: (submissionId) => api.get(`/ai-feedback/submission/${submissionId}`),
    regenerate: (submissionId) => api.post(`/ai-feedback/submission/${submissionId}/regenerate`),
};

// Rooms API
export const roomsAPI = {
    create: (data) => api.post("/rooms/", data),
    getByCode: (roomCode) => api.get(`/rooms/${roomCode}`),
    join: (roomCode, data = {}) => api.post(`/rooms/${roomCode}/join`, data),
    leave: (roomCode) => api.post(`/rooms/${roomCode}/leave`),
    getUserRooms: () => api.get("/rooms/"),
    getParticipants: (roomCode) => api.get(`/rooms/${roomCode}/participants`),
    getMessages: (roomCode, limit = 50) => api.get(`/rooms/${roomCode}/messages`, { params: { limit } }),
    sendMessage: (roomCode, content) => api.post(`/rooms/${roomCode}/messages`, { content }),
    update: (roomCode, data) => api.put(`/rooms/${roomCode}`, data),
    runCode: (roomCode, data) => api.post(`/rooms/${roomCode}/execute`, data),
    runTests: (roomCode, data) => api.post(`/rooms/${roomCode}/run-tests`, data),
};

// Dashboard API
export const dashboardAPI = {
    getStats: () => api.get("/dashboard/stats"),
    getLeaderboard: (limit = 10) => api.get("/dashboard/leaderboard", { params: { limit } }),
};

// WebSocket URL
export const WS_BASE_URL = "ws://127.0.0.1:8000";

// Helper functions
export const setAuthToken = (token) => {
    localStorage.setItem("access_token", token);
};

export const getAuthToken = () => {
    return localStorage.getItem("access_token");
};

export const removeAuthToken = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
};

export const setUser = (user) => {
    localStorage.setItem("user", JSON.stringify(user));
};

export const getUser = () => {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
};

export const isAuthenticated = () => {
    return !!getAuthToken();
};

export default api;
