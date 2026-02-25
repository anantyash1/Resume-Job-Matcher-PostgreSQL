
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Building2, LogOut, Users, FileText, Clock, CheckCircle,
  XCircle, Eye, Filter, TrendingUp, Star, Search,
  Plus, Edit2, Trash2, ChevronDown, X, Save, Briefcase
} from 'lucide-react';
import {
  getCurrentCompany, getCompanyApplications,
  updateApplicationStatus, viewResumeDetails, downloadResume
} from '../services/api';
import ResumeViewerModal from '../components/ResumeViewerModal';
import api from '../services/api';
import { IoArrowBackSharp } from "react-icons/io5";

const HRDashboard = () => {
  const navigate = useNavigate();

  // State
  const [company, setCompany] = useState(null);
  const [applications, setApplications] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('applications');
  const [statusFilter, setStatusFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedResume, setSelectedResume] = useState(null);
  const [selectedApplicant, setSelectedApplicant] = useState(null);
  const [stats, setStats] = useState({ total: 0, pending: 0, shortlisted: 0, rejected: 0 });

  // Job form state
  const [showJobForm, setShowJobForm] = useState(false);
  const [editingJob, setEditingJob] = useState(null);
  const [jobForm, setJobForm] = useState({
    title: '', location: '', description: '',
    requirements: '', salary_range: '', job_type: 'Full-time'
  });
  const [jobFormLoading, setJobFormLoading] = useState(false);
  const [jobFormError, setJobFormError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, [statusFilter, searchQuery]);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [companyData, appsData, jobsData] = await Promise.all([
        getCurrentCompany(),
        getCompanyApplications(statusFilter || null, searchQuery || null),
        getHRJobs()
      ]);
      setCompany(companyData);
      setApplications(appsData);
      setJobs(jobsData);
      setStats({
        total: appsData.length,
        pending: appsData.filter(a => a.status === 'pending').length,
        shortlisted: appsData.filter(a => a.status === 'shortlisted').length,
        rejected: appsData.filter(a => a.status === 'rejected').length
      });
    } catch (error) {
      if (error.response?.status === 401) navigate('/hr/login');
    } finally {
      setLoading(false);
    }
  };

  const getHRJobs = async () => {
    try {
      const response = await api.get('/hr/jobs');
      return response.data;
    } catch {
      return [];
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('hrToken');
    localStorage.removeItem('token');
    navigate('/hr/login');
  };

  const handleStatusChange = async (appId, newStatus) => {
    try {
      await updateApplicationStatus(appId, newStatus);
      loadDashboardData();
    } catch {
      alert('Failed to update status');
    }
  };

  // Job CRUD
  const openCreateJob = () => {
    setEditingJob(null);
    setJobForm({ title: '', location: '', description: '', requirements: '', salary_range: '', job_type: 'Full-time' });
    setJobFormError('');
    setShowJobForm(true);
  };

  const openEditJob = (job) => {
    setEditingJob(job);
    setJobForm({
      title: job.title,
      location: job.location || '',
      description: job.description,
      requirements: job.requirements || '',
      salary_range: job.salary_range || '',
      job_type: job.job_type || 'Full-time'
    });
    setJobFormError('');
    setShowJobForm(true);
  };

  const handleJobFormSubmit = async (e) => {
    e.preventDefault();
    setJobFormLoading(true);
    setJobFormError('');
    try {
      if (editingJob) {
        await api.put(`/hr/jobs/${editingJob.id}`, jobForm);
      } else {
        await api.post('/hr/jobs', jobForm);
      }
      setShowJobForm(false);
      loadDashboardData();
    } catch (err) {
      setJobFormError(err.response?.data?.detail || 'Failed to save job');
    } finally {
      setJobFormLoading(false);
    }
  };

  const handleDeleteJob = async (jobId) => {
    if (!window.confirm('Delete this job posting?')) return;
    try {
      await api.delete(`/hr/jobs/${jobId}`);
      loadDashboardData();
    } catch {
      alert('Failed to delete job');
    }
  };

  const getStatusBadge = (s) => {
    const cfg = {
      pending: { cls: 'bg-yellow-900/30 text-yellow-300 border-yellow-800/50', icon: Clock },
      reviewed: { cls: 'bg-blue-900/30 text-blue-300 border-blue-800/50', icon: Eye },
      shortlisted: { cls: 'bg-green-900/30 text-green-300 border-green-800/50', icon: CheckCircle },
      rejected: { cls: 'bg-red-900/30 text-red-300 border-red-800/50', icon: XCircle }
    };
    const { cls, icon: Icon } = cfg[s] || cfg.pending;
    return (
      <span className={`px-3 py-1 rounded-lg text-xs font-semibold border ${cls} flex items-center gap-1 w-fit`}>
        <Icon className="h-3 w-3" />
        {s.charAt(0).toUpperCase() + s.slice(1)}
      </span>
    );
  };

  const getMatchBadge = (score) => {
    if (!score) return <span className="text-gray-500 text-xs">N/A</span>;
    const pct = (score * 100).toFixed(0);
    const color = score >= 0.7 ? 'from-green-500 to-emerald-500'
      : score >= 0.5 ? 'from-yellow-500 to-orange-500'
      : 'from-red-500 to-orange-500';
    return (
      <span className={`px-2 py-1 rounded-lg bg-gradient-to-r ${color}/20 text-white text-xs font-bold border border-white/10`}>
        {pct}%
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900">
      <button onClick={() => navigate(-1)} className="absolute top-4 left-4 text-red-500 hover:text-red-400">
                <IoArrowBackSharp className="h-6 w-6" />
                </button>
      {/* Navbar */}
      <nav className="bg-gray-900/80 backdrop-blur-md border-b border-gray-800 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 flex justify-between items-center h-16">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-pink-500 blur-lg opacity-40"></div>
              <Building2 className="h-8 w-8 text-red-400 relative z-10" />
            </div>
            <div>
              <p className="text-white font-bold text-lg leading-none">{company?.name}</p>
              <p className="text-gray-500 text-xs">HR Dashboard</p>
            </div>
          </div>
          <button onClick={handleLogout} className="flex items-center gap-2 text-gray-400 hover:text-red-400 transition-colors text-sm">
            <LogOut className="h-4 w-4" /> Logout
          </button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Total', value: stats.total, icon: Users, color: 'from-purple-500 to-pink-500' },
            { label: 'Pending', value: stats.pending, icon: Clock, color: 'from-yellow-500 to-orange-500' },
            { label: 'Shortlisted', value: stats.shortlisted, icon: Star, color: 'from-green-500 to-emerald-500' },
            { label: 'Rejected', value: stats.rejected, icon: XCircle, color: 'from-red-500 to-pink-500' }
          ].map((s, i) => (
            <div key={i} className="card glow-effect py-5 hover:scale-105 transition-transform">
              <div className={`p-2 rounded-lg bg-gradient-to-r ${s.color}/20 w-fit mb-3`}>
                <s.icon className="h-5 w-5 text-white" />
              </div>
              <p className="text-3xl font-bold text-white">{s.value}</p>
              <p className="text-gray-400 text-sm">{s.label}</p>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-gray-800">
          {['applications', 'jobs'].map(tab => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 font-semibold text-sm capitalize transition-all border-b-2 ${
                activeTab === tab
                  ? 'border-red-500 text-red-400'
                  : 'border-transparent text-gray-500 hover:text-gray-300'
              }`}>
              {tab === 'applications' ? <><Users className="inline h-4 w-4 mr-1" />Applications</> : <><Briefcase className="inline h-4 w-4 mr-1" />My Jobs</>}
            </button>
          ))}
        </div>

        {/* APPLICATIONS TAB */}
        {activeTab === 'applications' && (
          <div>
            {/* Search + Filter */}
            <div className="flex flex-wrap gap-3 mb-6">
              <div className="relative flex-1 min-w-64">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by name, email, or skill..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="input-field pl-10 py-2.5"
                />
                {searchQuery && (
                  <button onClick={() => setSearchQuery('')} className="absolute right-3 top-3 text-gray-400 hover:text-white">
                    <X className="h-4 w-4" />
                  </button>
                )}
              </div>
              <div className="flex gap-2 flex-wrap">
                {['', 'pending', 'shortlisted', 'reviewed', 'rejected'].map(s => (
                  <button key={s} onClick={() => setStatusFilter(s)}
                    className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                      statusFilter === s
                        ? 'bg-gradient-to-r from-red-600 to-pink-600 text-white'
                        : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                    }`}>
                    {s === '' ? 'All' : s.charAt(0).toUpperCase() + s.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Applications Table */}
            <div className="card glow-effect overflow-hidden p-0">
              {loading ? (
                <div className="flex justify-center items-center h-48">
                  <div className="relative h-12 w-12">
                    <div className="absolute inset-0 border-4 border-gray-800 rounded-full"></div>
                    <div className="absolute inset-0 border-4 border-t-red-500 rounded-full animate-spin"></div>
                  </div>
                </div>
              ) : applications.length === 0 ? (
                <div className="text-center py-16 p-8">
                  <Users className="h-12 w-12 text-gray-600 mx-auto mb-3" />
                  <p className="text-gray-400">No applications found</p>
                  <p className="text-gray-600 text-sm mt-1">
                    {searchQuery ? 'Try a different search term' : 'Applications will appear when candidates apply'}
                  </p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-900/50 border-b border-gray-800">
                      <tr>
                        {['Candidate', 'Position', 'Match', 'Skills', 'Applied', 'Status', 'Actions'].map(h => (
                          <th key={h} className="text-left py-4 px-4 text-gray-400 text-sm font-semibold">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {applications.map(app => (
                        <tr key={app.id} className="border-b border-gray-800/50 hover:bg-white/2 transition-colors">
                          <td className="py-4 px-4">
                            <p className="text-white font-semibold text-sm">{app.user_name}</p>
                            <p className="text-gray-500 text-xs">{app.user_email}</p>
                          </td>
                          <td className="py-4 px-4 text-gray-300 text-sm">{app.job_title}</td>
                          <td className="py-4 px-4">{getMatchBadge(app.similarity_score)}</td>
                          <td className="py-4 px-4">
                            <div className="flex flex-wrap gap-1">
                              {app.skills.slice(0, 2).map((sk, i) => (
                                <span key={i} className="px-2 py-0.5 bg-red-900/30 text-red-300 rounded text-xs">{sk}</span>
                              ))}
                              {app.skills.length > 2 && (
                                <span className="px-2 py-0.5 bg-gray-800 text-gray-400 rounded text-xs">+{app.skills.length - 2}</span>
                              )}
                            </div>
                          </td>
                          <td className="py-4 px-4 text-gray-500 text-xs">
                            {new Date(app.applied_at).toLocaleDateString()}
                          </td>
                          <td className="py-4 px-4">{getStatusBadge(app.status)}</td>
                          <td className="py-4 px-4">
                            <div className="flex gap-2">
                              {app.status === 'pending' && (
                                <>
                                  <button onClick={() => handleStatusChange(app.id, 'shortlisted')}
                                    title="Shortlist"
                                    className="p-1.5 bg-green-900/30 hover:bg-green-900/50 text-green-300 rounded-lg transition-colors">
                                    <CheckCircle className="h-4 w-4" />
                                  </button>
                                  <button onClick={() => handleStatusChange(app.id, 'rejected')}
                                    title="Reject"
                                    className="p-1.5 bg-red-900/30 hover:bg-red-900/50 text-red-300 rounded-lg transition-colors">
                                    <XCircle className="h-4 w-4" />
                                  </button>
                                </>
                              )}
                              <button onClick={() => { setSelectedResume(app.resume_id); setSelectedApplicant(app.user_name); }}
                                title="View Resume"
                                className="p-1.5 bg-blue-900/30 hover:bg-blue-900/50 text-blue-300 rounded-lg transition-colors">
                                <Eye className="h-4 w-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* JOBS TAB */}
        {activeTab === 'jobs' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <p className="text-gray-400">{jobs.length} job posting{jobs.length !== 1 ? 's' : ''}</p>
              <button onClick={openCreateJob}
                className="flex items-center gap-2 bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white px-5 py-2.5 rounded-xl font-semibold transition-all">
                <Plus className="h-4 w-4" /> Post New Job
              </button>
            </div>

            {jobs.length === 0 ? (
              <div className="card text-center py-16 glow-effect">
                <Briefcase className="h-12 w-12 text-gray-600 mx-auto mb-3" />
                <p className="text-gray-400">No jobs posted yet</p>
                <button onClick={openCreateJob} className="mt-4 btn-primary">Post Your First Job</button>
              </div>
            ) : (
              <div className="grid gap-4">
                {jobs.map(job => (
                  <div key={job.id} className="card glow-effect hover:border-red-500/30 transition-all">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-xl font-bold text-white">{job.title}</h3>
                          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${job.is_active ? 'bg-green-900/30 text-green-300' : 'bg-gray-800 text-gray-400'}`}>
                            {job.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </div>
                        <div className="flex flex-wrap gap-4 text-sm text-gray-400 mb-3">
                          {job.location && <span>📍 {job.location}</span>}
                          <span>💼 {job.job_type}</span>
                          {job.salary_range && <span>💰 {job.salary_range}</span>}
                          <span>📅 {new Date(job.posted_date).toLocaleDateString()}</span>
                        </div>
                        <p className="text-gray-300 text-sm line-clamp-2">{job.description}</p>
                      </div>
                      <div className="flex gap-2 ml-4">
                        <button onClick={() => openEditJob(job)}
                          className="p-2 bg-blue-900/30 hover:bg-blue-900/50 text-blue-300 rounded-lg transition-colors" title="Edit">
                          <Edit2 className="h-4 w-4" />
                        </button>
                        <button onClick={() => handleDeleteJob(job.id)}
                          className="p-2 bg-red-900/30 hover:bg-red-900/50 text-red-300 rounded-lg transition-colors" title="Delete">
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Job Form Modal */}
      {showJobForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="w-full max-w-2xl bg-gradient-to-br from-gray-900 via-black to-gray-900 rounded-2xl border border-gray-800 shadow-2xl overflow-hidden">
            <div className="flex items-center justify-between p-6 border-b border-gray-800">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <Briefcase className="h-5 w-5 text-red-400" />
                {editingJob ? 'Edit Job' : 'Post New Job'}
              </h2>
              <button onClick={() => setShowJobForm(false)} className="p-2 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-white">
                <X className="h-5 w-5" />
              </button>
            </div>
            <form onSubmit={handleJobFormSubmit} className="p-6 space-y-4 overflow-y-auto max-h-[75vh]">
              {jobFormError && (
                <div className="bg-red-900/20 border border-red-500/50 text-red-300 p-3 rounded-lg text-sm">{jobFormError}</div>
              )}
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1.5">Job Title *</label>
                  <input type="text" value={jobForm.title} onChange={e => setJobForm({...jobForm, title: e.target.value})} required className="input-field" placeholder="Senior React Developer" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1.5">Location</label>
                  <input type="text" value={jobForm.location} onChange={e => setJobForm({...jobForm, location: e.target.value})} className="input-field" placeholder="Remote / New York, NY" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1.5">Job Type</label>
                  <select value={jobForm.job_type} onChange={e => setJobForm({...jobForm, job_type: e.target.value})} className="input-field">
                    <option>Full-time</option>
                    <option>Part-time</option>
                    <option>Contract</option>
                    <option>Internship</option>
                    <option>Remote</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1.5">Salary Range</label>
                  <input type="text" value={jobForm.salary_range} onChange={e => setJobForm({...jobForm, salary_range: e.target.value})} className="input-field" placeholder="$80,000 - $120,000" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">Description *</label>
                <textarea value={jobForm.description} onChange={e => setJobForm({...jobForm, description: e.target.value})} required rows={4} className="input-field resize-none" placeholder="Describe the role, responsibilities..." />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">Requirements</label>
                <textarea value={jobForm.requirements} onChange={e => setJobForm({...jobForm, requirements: e.target.value})} rows={4} className="input-field resize-none" placeholder="List required skills, experience, qualifications..." />
              </div>
              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => setShowJobForm(false)} className="flex-1 btn-secondary">Cancel</button>
                <button type="submit" disabled={jobFormLoading} className="flex-1 btn-primary flex items-center justify-center gap-2">
                  {jobFormLoading ? 'Saving...' : <><Save className="h-4 w-4" />{editingJob ? 'Update Job' : 'Post Job'}</>}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Resume Viewer Modal */}
      <ResumeViewerModal
        resumeId={selectedResume}
        applicantName={selectedApplicant}
        isOpen={!!selectedResume}
        onClose={() => { setSelectedResume(null); setSelectedApplicant(null); }}
      />
    </div>
  );
};

export default HRDashboard;
