// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// import Landing from './pages/landing';
// import Login from './pages/login';
// import Register from './pages/Register';
// import Dashboard from './pages/Dashboard';
// import HRLogin from './pages/HRLogin';
// import HRDashboard from './pages/HRDashboard';


// function App() {
//   const isAuthenticated = () => {
//     return localStorage.getItem('token') !== null;
//   };

//   const isHRAuthenticated = () => {
//     return localStorage.getItem('hrToken') !== null;
//   };

//   const PrivateRoute = ({ children }) => {
//     return isAuthenticated() ? children : <Navigate to="/login" />;
//   };

//   const HRPrivateRoute = ({ children }) => {
//     return isHRAuthenticated() ? children : <Navigate to="/hr/login" />;
//   };

//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<Landing />} />
//         <Route path="/login" element={<Login />} />
//         <Route path="/register" element={<Register />} />
//         <Route path="/hr/login" element={<HRLogin />} />
//         <Route 
//           path="/dashboard" 
//           element={
//             <PrivateRoute>
//               <Dashboard />
//             </PrivateRoute>
//           } 
//         />
//         <Route 
//           path="/hr/dashboard" 
//           element={
//             <HRPrivateRoute>
//               <HRDashboard />
//             </HRPrivateRoute>
//           } 
//         />
//       </Routes>
//     </Router>
//   );
// }

// export default App;



import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './pages/landing';
import Login from './pages/login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import HRLogin from './pages/HRLogin';
import HRRegister from './pages/HRRegister';
import HRDashboard from './pages/HRDashboard';

function App() {
  const isAuthenticated = () => !!localStorage.getItem('token');
  const isHRAuthenticated = () => !!localStorage.getItem('hrToken');

  const PrivateRoute = ({ children }) =>
    isAuthenticated() ? children : <Navigate to="/login" />;

  const HRPrivateRoute = ({ children }) =>
    isHRAuthenticated() ? children : <Navigate to="/hr/login" />;

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/hr/login" element={<HRLogin />} />
        <Route path="/hr/register" element={<HRRegister />} />
        <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/hr/dashboard" element={<HRPrivateRoute><HRDashboard /></HRPrivateRoute>} />
      </Routes>
    </Router>
  );
}

export default App;