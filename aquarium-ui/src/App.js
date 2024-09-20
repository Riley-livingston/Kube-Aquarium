import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AquariumDashboard from './AquariumDashboard';
import './App.css';

function App() {
  const [aquariumStatus, setAquariumStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        console.log('Fetching aquarium status...');
        const response = await axios.get('/api/aquarium_status');
        console.log('Aquarium status response:', response.data);
        setAquariumStatus(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching aquarium status:', error);
        console.error('Error details:', error.response ? error.response.data : 'No response data');
        setError(`Failed to load aquarium status. ${error.message}`);
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="App">Loading...</div>;
  }

  if (error) {
    return <div className="App">Error: {error}</div>;
  }

  return (
    <div className="App">
      <h1>Kubernetes Aquarium</h1>
      <AquariumDashboard />
      <div className="aquarium">
        {Array.isArray(aquariumStatus?.fish) && aquariumStatus.fish.length > 0 ? (
          aquariumStatus.fish.map(fish => (
            <div
              key={fish.id}
              className="fish"
              style={{
                left: `${fish.position.x}%`,
                top: `${fish.position.y}%`,
                backgroundColor: fish.health > 50 ? 'goldenrod' : 'orange',
              }}
            />
          ))
        ) : (
          <p>No fish data available.</p>
        )}
      </div>
    </div>
  );
}

export default App;