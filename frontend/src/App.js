// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './components/Authentication/Login';
import CreateUser from './components/UserManagement/CreateUser';
import EditUser from './components/UserManagement/EditUser';
import UsersList from './components/UserManagement/UsersList';
import UploadFaceImage from './components/FaceRecognition/UploadFaceImage';
import RecordAttendance from './components/AttendanceTracking/RecordAttendance';
import ViewAttendance from './components/AttendanceTracking/ViewAttendance';
import AttendanceAlerts from './components/Notifications/AttendanceAlerts';
import AttendanceDashboard from './components/Analytics/AttendanceDashboard';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <div>
          <h1>Face Recognition Attendance System</h1>
          <nav>
            <ul>
              <li>
                <Link to="/login">Login</Link>
              </li>
              <li>
                <Link to="/users">Users</Link>
              </li>
              <li>
                <Link to="/face-recognition/upload">Upload Face Image</Link>
              </li>
              <li>
                <Link to="/attendance">Attendance</Link>
              </li>
              <li>
                <Link to="/notifications">Notifications</Link>
              </li>
              <li>
                <Link to="/analytics">Analytics</Link>
              </li>
            </ul>
          </nav>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/users/create" element={<CreateUser />} />
            <Route path="/users/:userId/edit" element={<EditUser />} />
            <Route path="/users" element={<UsersList />} />
            <Route path="/face-recognition/upload" element={<UploadFaceImage />} />
            <Route path="/attendance/record" element={<RecordAttendance />} />
            <Route path="/attendance" element={<ViewAttendance />} />
            <Route path="/notifications" element={<AttendanceAlerts />} />
            <Route path="/analytics" element={<AttendanceDashboard />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
};

export default App;
