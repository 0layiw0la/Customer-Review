import React, { useState } from 'react';

function ReviewForm({ onDataReceived }) {
  const [businessName, setBusinessName] = useState('');
  const [locationName, setLocationName] = useState('');
  const [loading, setLoading] = useState(false); // New loading state

  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true); // Start loading

    // Make API request to fetch reviews
    fetch('https://customereeviewapp-bjdzasdpemesc4g0.canadacentral-01.azurewebsites.net/get_reviews', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        business_name: businessName,
        location_name: locationName,
      }),
    })
      .then(response => response.json())
      .then(data => {
        setLoading(false); // Stop loading
        if (data.error) {
          alert(data.error);
        } else {
          onDataReceived(data);
        }
      })
      .catch(error => {
        setLoading(false); // Stop loading
        console.error('Error:', error);
        alert('There was an error fetching the reviews.');
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit} id="review-form">
        <input
          id="business_name"
          type="text"
          placeholder="Business Name"
          value={businessName}
          onChange={(e) => setBusinessName(e.target.value)}
          required
        />
        <input
          id="location"
          type="text"
          placeholder="Location"
          value={locationName}
          onChange={(e) => setLocationName(e.target.value)}
          required
        />
        <button id="review_btn" type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Get Reviews'}
        </button>
      </form>

      {/* Show loading spinner */}
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Fetching reviews...</p>
        </div>
      )}
    </div>
  );
}

export default ReviewForm;
