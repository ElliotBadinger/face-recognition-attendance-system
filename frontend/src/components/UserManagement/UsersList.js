// Component for displaying a list of users
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const UsersList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Fetch users data from backend
    // Update users state with fetched data
    // For demo purposes, using placeholder data
    const placeholderData = [
      { id: 1, username: 'user1', role: 'admin' },
      { id: 2, username: 'user2', role: 'employee' },
      { id: 3, username: 'user3', role: 'employee' },
    ];
    setUsers(placeholderData);
  }, []);

  return (
    <div>
      <h2>Users</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.role}</td>
              <td>
                <Link to={`/users/${user.id}/edit`}>Edit</Link>
                {/* Add Delete button here */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UsersList;
