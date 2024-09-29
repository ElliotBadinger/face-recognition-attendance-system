// Component for viewing attendance records
import React, { useState, useEffect } from 'react';

const ViewAttendance = () => {
  const [attendanceData, setAttendanceData] = useState([]);

  useEffect(() => {
    // Fetch attendance data from backend
    // Update attendanceData state with fetched data
    // For demo purposes, using placeholder data
    const placeholderData = [
      {
        id: 1,
        date: '2023-12-20',
        username: 'user1',
        timeIn: '09:00 AM',
        timeOut: '05:00 PM',
        status: 'Present',
      },
      {
        id: 2,
        date: '2023-12-20',
        username: 'user2',
        timeIn: '09:15 AM',
        timeOut: '05:30 PM',
        status: 'Present',
      },
      {
        id: 3,
        date: '2023-12-19',
        username: 'user3',
        timeIn: '09:00 AM',
        timeOut: '05:00 PM',
        status: 'Present',
      },
    ];
    setAttendanceData(placeholderData);
  }, []);

  return (
    <div>
      <h2>Attendance Records</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Username</th>
            <th>Time In</th>
            <th>Time Out</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {attendanceData.map((record) => (
            <tr key={record.id}>
              <td>{record.date}</td>
              <td>{record.username}</td>
              <td>{record.timeIn}</td>
              <td>{record.timeOut}</td>
              <td>{record.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ViewAttendance;
