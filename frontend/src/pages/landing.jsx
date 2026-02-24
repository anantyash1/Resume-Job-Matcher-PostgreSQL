
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Briefcase, Target, Zap, Shield, Sparkles, ArrowRight } from 'lucide-react';
import Footer from '../components/Footer';

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-900 via-black to-gray-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 bg-gradient-to-r from-red-500/5 via-pink-500/5 to-red-600/5 animate-pulse"></div>
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-red-500/10 via-transparent to-transparent"></div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 relative z-10">
          <div className="text-center">
            <div className="flex justify-center mb-6 relative">
              <div className="absolute inset-0 bg-red-500 blur-3xl opacity-20"></div>
              <Briefcase className="h-20 w-20 text-red-500 relative z-10 animate-bounce" />
              <Sparkles className="absolute -top-2 -right-2 h-6 w-6 text-pink-500 animate-ping" />
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="bg-gradient-to-r from-red-500 via-pink-500 to-red-600 bg-clip-text text-transparent">
                Find Your Perfect
              </span>
              <br />
              <span className="text-white">Job Match</span>
            </h1>
            
            <p className="text-xl md:text-2xl mb-8 text-gray-300 max-w-3xl mx-auto">
              Upload your resume and get intelligent job recommendations powered by 
              <span className="neon-text font-bold"> AI-powered matching algorithms</span>
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
  <button
    onClick={() => navigate('/register')}
    className="bg-white text-blue-600 font-bold py-3 px-8 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105"
  >
    Get Started Free
  </button>
  
  <button
    onClick={() => navigate('/login')}
    className="bg-transparent border-2 border-white text-white font-bold py-3 px-8 rounded-lg hover:bg-white hover:text-blue-600 transition-all duration-200"
  >
    Sign In
  </button>
  
  <button
    onClick={() => navigate('/hr/login')}
    className="bg-gradient-to-r from-red-600 to-pink-600 text-white font-bold py-3 px-8 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105"
  >
    HR Portal
  </button>
</div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/50 to-black"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <h2 className="text-4xl font-bold text-center mb-16">
            <span className="neon-text">Why Choose JobMatch?</span>
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Target,
                color: 'red',
                title: 'AI-Powered Matching',
                desc: 'Advanced algorithms ensure you get the most relevant job recommendations based on your skills'
              },
              {
                icon: Zap,
                color: 'pink',
                title: 'Lightning Fast',
                desc: 'Get instant job recommendations within seconds of uploading your resume. No waiting, just results'
              },
              {
                icon: Shield,
                color: 'red',
                title: '100% Private',
                desc: 'Your resume data stays secure and is never shared with third parties. Complete privacy guaranteed'
              }
            ].map((feature, index) => (
              <div key={index} className="card glow-effect group">
                <div className={`bg-gradient-to-br from-${feature.color}-900/20 to-${feature.color}-600/10 rounded-2xl w-20 h-20 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className={`h-10 w-10 text-${feature.color}-500`} />
                </div>
                <h3 className="text-2xl font-bold text-white mb-4">
                  {feature.title}
                </h3>
                <p className="text-gray-400">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="py-20 relative">
        <div className="absolute inset-0 bg-gradient-to-t from-red-500/5 via-transparent to-transparent"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <h2 className="text-4xl font-bold text-center mb-16">
            <span className="neon-text">How It Works</span>
          </h2>
          
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { step: 1, title: 'Create Account', desc: 'Sign up for free in 30 seconds' },
              { step: 2, title: 'Upload Resume', desc: 'Upload PDF, DOC, or any format' },
              { step: 3, title: 'AI Processing', desc: 'Advanced AI extracts skills & keywords' },
              { step: 4, title: 'Get Matches', desc: 'Receive perfect job recommendations' },
            ].map((item) => (
              <div key={item.step} className="text-center relative group">
                <div className="relative mb-6">
                  <div className="absolute inset-0 bg-gradient-to-r from-red-600 to-pink-600 blur-lg opacity-50 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <div className="bg-gradient-to-br from-red-600 via-pink-600 to-red-700 text-white rounded-2xl w-16 h-16 flex items-center justify-center mx-auto relative font-bold text-2xl shadow-lg shadow-red-500/30 group-hover:scale-110 transition-transform duration-300">
                    {item.step}
                  </div>
                </div>
                <h3 className="text-xl font-bold text-white mb-3 group-hover:text-red-400 transition-colors duration-300">
                  {item.title}
                </h3>
                <p className="text-gray-400">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 relative">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <div className="card glow-effect">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              <span className="neon-text">Ready to Transform Your Career?</span>
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of professionals who found their dream jobs through JobMatch
            </p>
            <button
              onClick={() => navigate('/register')}
              className="btn-primary glow-effect text-lg px-10 py-4"
            >
              Start Your Journey Now
            </button>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Landing;