// Component for editing an existing user
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const EditUser = () => {
  const { userId } = useParams();
  const [formData, setFormData] = useState({});

  useEffect(() => {
    // Fetch user data based on userId from backend
    // Update formData with fetched data
    // For demo purposes, using placeholder data
    const placeholderData = {
      username: 'user' + userId,
      role: 'employee',
    };
    setFormData(placeholderData);
  }, [userId]);

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission, send updated data to backend
    console.log(formData);
    // Reset form after submission
    setFormData({});
  };

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  return (
    <div>
      <h2>Edit User</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username || ''}
            onChange={handleChange}
          />
        </div>
        <div>
          <label htmlFor="role">Role:</label>
          <select id="role" name="role" value={formData.role || ''} onChange={handleChange}>
            <option value="admin">Admin</option>
            <option value="employee">Employee</option>
          </select>
        </div>
        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
};

export default EditUser;
