// Component for displaying attendance alerts
import React, { useState, useEffect } from 'react';

const AttendanceAlerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // Fetch attendance alerts from backend
    // Update alerts state with fetched data
    // For demo purposes, using placeholder data
    const placeholderData = [
      { id: 1, message: 'User1 was late today.', timestamp: '2023-12-20 09:15 AM' },
      { id: 2, message: 'User2 is absent today.', timestamp: '2023-12-20 09:00 AM' },
    ];
    setAlerts(placeholderData);
  }, []);

  return (
    <div>
      <h2>Attendance Alerts</h2>
      <ul>
        {alerts.map((alert) => (
          <li key={alert.id}>
            {alert.message} - {alert.timestamp}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AttendanceAlerts;
