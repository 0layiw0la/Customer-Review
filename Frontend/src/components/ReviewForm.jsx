import React, { useState } from 'react';

function ReviewForm({ onDataReceived }) {
  const [businessName, setBusinessName] = useState('');
  const [locationName, setLocationName] = useState('');
  const [loading, setLoading] = useState(false); // Setting up a state to track loading

  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true); // Setting loading to true when the form is being submitted

    // Making an API request to fetch reviews from the server
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
        setLoading(false); 
        if (data.error) {
          alert(data.error); // Displaying an error message if there is any
        } else {
          onDataReceived(data); 
        }
      })
      .catch(error => {
        setLoading(false); // Stopping the loading process if an error occurs
        console.error('Error:', error); // Logging the error
        alert('There was an error fetching the reviews. Check network connection'); // Displaying an error message
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
          {loading ? 'Loading...' : 'Get Reviews'} {/* Changing the button text based on loading state */}
        </button>
      </form>

      {/* Showing the loading spinner when the data is being fetched */}
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
