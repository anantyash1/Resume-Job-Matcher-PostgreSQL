
//dashboard.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import ResumeUploader from '../components/ResumeUploader';
import JobCard from '../components/JobCard';
import { getCurrentUser, getMyResumes, getJobRecommendations } from '../services/api';
import { Loader, FileText, Briefcase, Sparkles, Target, Zap, TrendingUp, User, Star, ArrowRight } from 'lucide-react';
import { IoArrowBackSharp } from "react-icons/io5";

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [selectedResume, setSelectedResume] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    matchRate: 0,
    avgSalary: 0,
    totalJobs: 0
  });

  useEffect(() => {
    loadUserData();
    // Stats animation
    const interval = setInterval(() => {
      if (stats.matchRate < 85) {
        setStats(prev => ({
          ...prev,
          matchRate: Math.min(prev.matchRate + 1, 85),
          avgSalary: Math.min(prev.avgSalary + 1000, 85000),
          totalJobs: Math.min(prev.totalJobs + 5, 1250)
        }));
      }
    }, 50);
    
    return () => clearInterval(interval);
  }, []);

  const loadUserData = async () => {
    try {
      const userData = await getCurrentUser();
      setUser(userData);
      
      const resumesData = await getMyResumes();
      setResumes(resumesData);
      
      if (resumesData.length > 0) {
        setSelectedResume(resumesData[0]);
        loadJobRecommendations(resumesData[0].id);
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const loadJobRecommendations = async (resumeId) => {
    setLoading(true);
    try {
      const recommendations = await getJobRecommendations(resumeId, 10);
      setJobs(recommendations);
    } catch (error) {
      console.error('Error loading job recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (newResume) => {
    setResumes([newResume, ...resumes]);
    setSelectedResume(newResume);
    loadJobRecommendations(newResume.id);
  };

  const handleResumeChange = (resumeId) => {
    const resume = resumes.find(r => r.id === resumeId);
    setSelectedResume(resume);
    loadJobRecommendations(resumeId);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-900 via-black to-gray-900">
      <button onClick={() => navigate(-1)} className="absolute top-4 left-4 text-red-500 hover:text-red-400">
                <IoArrowBackSharp className="h-6 w-6" />
                </button>
      {/* Animated Background Particles */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-red-500 rounded-full animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              opacity: Math.random() * 0.3 + 0.1
            }}
          />
        ))}
      </div>

      <Navbar user={user} />

      <div className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full relative z-10">
        {/* Welcome Section with Stats */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-pink-500 blur-xl opacity-50"></div>
                  <User className="h-10 w-10 text-red-400 relative z-10" />
                </div>
                <h1 className="text-4xl font-bold text-white">
                  Welcome back, <span className="neon-text">{user?.username}!</span>
                </h1>
              </div>
              <p className="text-gray-400 text-lg">
                Upload your resume to get personalized job recommendations powered by AI
              </p>
            </div>
            
            <Sparkles className="h-8 w-8 text-yellow-400 animate-pulse" />
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {[
              { 
                label: 'Match Rate', 
                value: `${stats.matchRate}%`, 
                icon: Target,
                color: 'from-red-500 to-pink-500',
                bg: 'bg-gradient-to-br from-red-900/20 to-red-800/10'
              },
              { 
                label: 'Avg Salary', 
                value: `$${stats.avgSalary.toLocaleString()}`, 
                icon: TrendingUp,
                color: 'from-pink-500 to-purple-500',
                bg: 'bg-gradient-to-br from-pink-900/20 to-purple-900/10'
              },
              { 
                label: 'Total Jobs', 
                value: `${stats.totalJobs}+`, 
                icon: Zap,
                color: 'from-purple-500 to-red-500',
                bg: 'bg-gradient-to-br from-purple-900/20 to-red-900/10'
              }
            ].map((stat, index) => (
              <div 
                key={index}
                className={`card glow-effect group ${stat.bg} hover:scale-[1.02] transition-all duration-500`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm mb-1">{stat.label}</p>
                    <p className={`text-3xl font-bold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}>
                      {stat.value}
                    </p>
                  </div>
                  <div className={`p-3 rounded-xl bg-gradient-to-br ${stat.color}/20`}>
                    <stat.icon className={`h-6 w-6 bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`} />
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-gray-800">
                  <div className="w-full bg-gray-800 rounded-full h-2">
                    <div 
                      className={`bg-gradient-to-r ${stat.color} h-2 rounded-full transition-all duration-1000 ease-out`}
                      style={{ width: `${stat.label === 'Match Rate' ? stats.matchRate : stat.label === 'Avg Salary' ? (stats.avgSalary / 85000 * 100) : (stats.totalJobs / 1250 * 100)}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Resume Upload & Selection */}
          <div className="lg:col-span-1 space-y-6">
            <ResumeUploader onUploadSuccess={handleUploadSuccess} />

            {resumes.length > 0 && (
              <div className="card glow-effect group hover:border-red-500/50">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-bold text-white flex items-center">
                    <FileText className="h-5 w-5 mr-2 text-red-400" />
                    Your Resumes
                  </h3>
                  <span className="px-3 py-1 bg-gradient-to-r from-red-900/50 to-pink-900/50 text-red-300 rounded-full text-sm">
                    {resumes.length} uploaded
                  </span>
                </div>
                
                <div className="space-y-3">
                  {resumes.map((resume) => (
                    <button
                      key={resume.id}
                      onClick={() => handleResumeChange(resume.id)}
                      className={`w-full text-left p-4 rounded-xl transition-all duration-300 group/item ${
                        selectedResume?.id === resume.id
                          ? 'bg-gradient-to-r from-red-900/30 via-pink-900/20 to-red-900/30 border-2 border-red-500/50 shadow-lg shadow-red-500/20'
                          : 'bg-gradient-to-r from-gray-900/50 to-gray-800/50 border border-gray-700 hover:border-red-400/30 hover:bg-gray-800/50'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1 min-w-0">
                          <p className="font-semibold text-white truncate group-hover/item:text-red-300 transition-colors">
                            {resume.filename}
                          </p>
                          <div className="flex items-center gap-2 mt-1">
                            <span className="text-sm text-gray-400">
                              {resume.skills.length} skills detected
                            </span>
                            <div className="flex">
                              {[...Array(Math.min(3, Math.floor(resume.skills.length / 5)))].map((_, i) => (
                                <Star key={i} className="h-3 w-3 text-yellow-500 fill-current" />
                              ))}
                            </div>
                          </div>
                        </div>
                        {selectedResume?.id === resume.id && (
                          <div className="ml-4 p-2 bg-gradient-to-r from-red-500 to-pink-500 rounded-full">
                            <div className="h-2 w-2 bg-white rounded-full"></div>
                          </div>
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {selectedResume && (
              <div className="card glow-effect">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-bold text-white">
                    <span className="flex items-center">
                      <Zap className="h-5 w-5 mr-2 text-yellow-400" />
                      Top Skills
                    </span>
                  </h3>
                  <span className="text-sm text-gray-400">
                    AI-extracted
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {selectedResume.skills.slice(0, 12).map((skill, index) => (
                    <span
                      key={index}
                      className="px-3 py-1.5 bg-gradient-to-r from-red-900/40 to-pink-900/40 text-red-300 rounded-lg text-sm font-medium border border-red-800/30 hover:scale-105 hover:border-red-500/50 transition-all duration-300 cursor-pointer group"
                    >
                      <span className="group-hover:text-white transition-colors">
                        {skill}
                      </span>
                    </span>
                  ))}
                  {selectedResume.skills.length > 12 && (
                    <span className="px-3 py-1.5 bg-gradient-to-r from-gray-800 to-gray-900 text-gray-400 rounded-lg text-sm border border-gray-700">
                      +{selectedResume.skills.length - 12} more
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Job Recommendations */}
          <div className="lg:col-span-2">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-bold text-white flex items-center mb-2">
                  <Briefcase className="h-8 w-8 mr-3 text-red-400" />
                  <span className="bg-gradient-to-r from-red-400 via-pink-400 to-red-400 bg-clip-text text-transparent">
                    AI Recommendations
                  </span>
                </h2>
                <p className="text-gray-400">
                  Personalized matches based on your resume
                </p>
              </div>
              {jobs.length > 0 && (
                <div className="flex items-center gap-2">
                  <div className="relative">
                    <div className="absolute inset-0 bg-red-500 blur-lg opacity-30"></div>
                    <span className="relative px-4 py-2 bg-gradient-to-r from-red-900/50 to-pink-900/50 text-red-300 rounded-xl border border-red-800/50 font-semibold">
                      {jobs.length} perfect matches
                    </span>
                  </div>
                </div>
              )}
            </div>

            {loading ? (
              <div className="flex flex-col justify-center items-center h-96">
                <div className="relative mb-8">
                  <div className="h-16 w-16 border-4 border-gray-800 rounded-full"></div>
                  <div className="absolute top-0 left-0 h-16 w-16 border-4 border-t-transparent border-red-500 rounded-full animate-spin"></div>
                  <div className="absolute top-0 left-0 h-16 w-16 border-4 border-r-transparent border-pink-500 rounded-full animate-spin" style={{ animationDelay: '-0.5s' }}></div>
                  <Sparkles className="absolute -top-2 -right-2 h-6 w-6 text-yellow-400 animate-ping" />
                </div>
                <p className="text-gray-400 text-lg">AI is analyzing your resume...</p>
                <p className="text-gray-500 text-sm mt-2">Finding the perfect matches for you</p>
              </div>
            ) : jobs.length > 0 ? (
              <div className="space-y-6">
                {jobs.map((job, index) => (
  <div 
    key={job.id}
    className="opacity-0 animate-fade-in"
    style={{ animationDelay: `${index * 100}ms` }}
  >
    <JobCard job={job} selectedResumeId={selectedResume?.id} />
  </div>
))}
                
                {/* View More Button */}
                <div className="flex justify-center pt-4">
                  <button className="group relative overflow-hidden bg-gradient-to-r from-gray-900 to-black border-2 border-gray-800 hover:border-red-500/50 text-white px-8 py-4 rounded-2xl font-semibold transition-all duration-500">
                    <span className="relative z-10 flex items-center gap-2">
                      View More Matches
                      <ArrowRight className="h-5 w-5 group-hover:translate-x-2 transition-transform" />
                    </span>
                    <div className="absolute inset-0 bg-gradient-to-r from-red-600/10 to-pink-600/10 translate-x-full group-hover:translate-x-0 transition-transform duration-500"></div>
                  </button>
                </div>
              </div>
            ) : (
              <div className="card text-center py-16 glow-effect">
                <div className="relative inline-block mb-6">
                  <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-pink-500 blur-3xl opacity-20"></div>
                  <Briefcase className="h-20 w-20 text-gray-400 mx-auto relative z-10" />
                </div>
                <h3 className="text-2xl font-semibold text-white mb-3">
                  No Recommendations Yet
                </h3>
                <p className="text-gray-400 mb-6 max-w-md mx-auto">
                  Upload your resume to unlock personalized job recommendations powered by our AI matching system
                </p>
                <div className="animate-bounce">
                  <ArrowRight className="h-8 w-8 text-red-500 mx-auto rotate-90" />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Floating Action Button */}
      <button className="fixed bottom-8 right-8 z-50 group">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-pink-500 rounded-full blur-lg opacity-70 group-hover:opacity-100 transition-opacity"></div>
          <div className="relative bg-gradient-to-r from-red-600 to-pink-600 text-white p-4 rounded-full shadow-2xl hover:shadow-red-500/30 hover:scale-110 transition-all duration-300">
            <Zap className="h-6 w-6" />
          </div>
          <div className="absolute -top-2 -right-2">
            <div className="h-4 w-4 bg-green-500 rounded-full animate-ping"></div>
          </div>
        </div>
      </button>

      <Footer />
    </div>
  );
};

export default Dashboard;