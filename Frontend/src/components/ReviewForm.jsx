import React, { useState } from 'react';

function ReviewForm({ onDataReceived }) {
  const [businessName, setBusinessName] = useState('');
  const [locationName, setLocationName] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Make API request to fetch reviews
    fetch('https://customer-review-59a9.onrender.com/', {
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
        if (data.error) {
          alert(data.error);
        } else {
          onDataReceived(data);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('There was an error fetching the reviews.');
      });
  };

  return (
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
      <button id="review_btn" type="submit">
        Get Reviews
      </button>
    </form>
  );
}

export default ReviewForm;
