import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Building2, AlertCircle, Eye, EyeOff } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

const HRRegister = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    description: '',
    website: '',
    industry: '',
    location: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/hr/register`, {
        name: formData.name,
        email: formData.email,
        password: formData.password,
        description: formData.description,
        website: formData.website,
        industry: formData.industry,
        location: formData.location
      });

      if (response.data) {
        navigate('/hr/login', {
          state: { message: 'Registration successful! Please login.' }
        });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-gray-900 via-black to-gray-900">
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {[...Array(15)].map((_, i) => (
          <div key={i} className="absolute w-1 h-1 bg-red-500 rounded-full animate-pulse"
            style={{ left: `${Math.random() * 100}%`, top: `${Math.random() * 100}%`, animationDelay: `${Math.random() * 5}s`, opacity: Math.random() * 0.3 + 0.1 }} />
        ))}
      </div>

      <div className="max-w-2xl w-full relative z-10">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-pink-500 blur-2xl opacity-50"></div>
              <Building2 className="h-16 w-16 text-red-400 relative z-10" />
            </div>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-red-400 via-pink-400 to-red-400 bg-clip-text text-transparent">
            Register Your Company
          </h1>
          <p className="text-gray-400 mt-2">Create your HR account to start hiring</p>
        </div>

        <div className="card glow-effect">
          {error && (
            <div className="mb-6 bg-red-900/20 border border-red-500/50 text-red-300 p-4 rounded-xl flex items-center gap-2">
              <AlertCircle className="h-5 w-5 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid md:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Company Name *</label>
                <input type="text" name="name" value={formData.name} onChange={handleChange} required className="input-field" placeholder="TechCorp Inc" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Company Email *</label>
                <input type="email" name="email" value={formData.email} onChange={handleChange} required className="input-field" placeholder="hr@company.com" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Password *</label>
                <div className="relative">
                  <input type={showPassword ? 'text' : 'password'} name="password" value={formData.password} onChange={handleChange} required className="input-field pr-12" placeholder="Min 8 characters" />
                  <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-3.5 text-gray-400 hover:text-white">
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Confirm Password *</label>
                <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} required className="input-field" placeholder="Re-enter password" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Industry</label>
                <select name="industry" value={formData.industry} onChange={handleChange} className="input-field">
                  <option value="">Select Industry</option>
                  <option value="Technology">Technology</option>
                  <option value="Finance">Finance</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Education">Education</option>
                  <option value="E-commerce">E-commerce</option>
                  <option value="Media">Media</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Location</label>
                <input type="text" name="location" value={formData.location} onChange={handleChange} className="input-field" placeholder="San Francisco, CA" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Website</label>
                <input type="url" name="website" value={formData.website} onChange={handleChange} className="input-field" placeholder="https://company.com" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Company Description</label>
              <textarea name="description" value={formData.description} onChange={handleChange} rows={3} className="input-field resize-none" placeholder="Brief description of your company..." />
            </div>

            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? 'Creating Account...' : 'Create HR Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-400">
              Already registered?{' '}
              <Link to="/hr/login" className="text-red-400 font-semibold hover:text-red-300">Sign In</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HRRegister;