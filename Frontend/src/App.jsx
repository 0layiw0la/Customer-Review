import React, { useState } from 'react';
import './App.css';
import ReviewForm from './components/ReviewForm';
import ReviewResults from './components/ReviewResults';

function App() {
  const [reviewsData, setReviewsData] = useState(null);

  const handleReviewData = (data) => {
    setReviewsData(data);
  };

  return (
    <div className="App">
      <h1>CUSTOMER REVIEWS</h1>
      <ReviewForm onDataReceived={handleReviewData} />
      {reviewsData && <ReviewResults data={reviewsData} />}
    </div>
  );
}

export default App;
