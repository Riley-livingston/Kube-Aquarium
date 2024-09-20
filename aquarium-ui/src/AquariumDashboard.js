import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AquariumDashboard.css';

function AquariumDashboard() {
  const [dashboardData, setDashboardData] = useState({
    fishCount: 0,
    cpuUsage: 0,  // Default value to prevent undefined error
    memoryUsage: 0,  // Default value to prevent undefined error
    healthyPods: 0,
    totalPods: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await axios.get('/api/dashboard_data');
        setDashboardData(response.data);
        setLoading(false); // Data loaded
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Failed to fetch dashboard data.');
        setLoading(false);
      }
    };

    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="aquarium-dashboard">Loading...</div>;
  }

  if (error) {
    return <div className="aquarium-dashboard">Error: {error}</div>;
  }

  return (
    <div className="aquarium-dashboard">
      <h2>Aquarium Dashboard</h2>
      <div className="stats-container">
        <div className="stat-item">
          <h3>Fish Count</h3>
          <p>{dashboardData.fishCount}</p>
        </div>
        <div className="stat-item">
          <h3>CPU Usage</h3>
          <p>{dashboardData.cpuUsage !== undefined ? dashboardData.cpuUsage.toFixed(2) : 'N/A'}%</p> {/* Safeguard */}
        </div>
        <div className="stat-item">
          <h3>Memory Usage</h3>
          <p>{dashboardData.memoryUsage !== undefined ? dashboardData.memoryUsage.toFixed(2) : 'N/A'}%</p> {/* Safeguard */}
        </div>
        <div className="stat-item">
          <h3>Pod Health</h3>
          <p>{dashboardData.healthyPods} / {dashboardData.totalPods}</p>
        </div>
      </div>
    </div>
  );
}

export default AquariumDashboard;
