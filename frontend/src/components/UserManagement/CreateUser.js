// Component for creating a new user
import React, { useState } from 'react';

const CreateUser = () => {
  const [formData, setFormData] = useState({});

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission, send data to backend
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
      <h2>Create New User</h2>
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
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password || ''}
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
        <button type="submit">Create User</button>
      </form>
    </div>
  );
};

export default CreateUser;
