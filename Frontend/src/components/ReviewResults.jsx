import React from 'react';

function ReviewResults({ data }) {
  const { positive_reviews, negative_reviews, avg_rating } = data;

  // Defining a function to handle the click event for expanding or collapsing reviews
  const handleToggle = (e) => {
    const reviewText = e.target.previousSibling; 
    const buttonText = e.target; 

    // Toggling the review text expansion
    if (reviewText.classList.contains('text')) {
      reviewText.classList.remove('text'); 
      reviewText.classList.add('extended'); 
      buttonText.textContent = 'Less'; 
    } else {
      reviewText.classList.remove('extended'); 
      reviewText.classList.add('text'); 
      buttonText.textContent = 'More'; 
    }
  };

  // Defining a function to render the reviews based on the type (positive or negative)
  const renderReviews = (reviews, reviewType) => {
    return Object.entries(reviews).map(([review, date], index) => (
      <div key={index} className="review">
        <div className="date">
          <i><b>{date}</b></i> {/* Displaying the review date */}
        </div>
        <div>
          <span className="text">{review}</span> {/* Displaying the review text */}
          <span
            className="toggle-button"
            onClick={handleToggle} // Adding a click handler to toggle the review text
          >
            More
          </span>
        </div>
      </div>
    ));
  };

  return (
    <div id="review-results">
      <div id="summary">
        Average Rating: <span id="avg-rating">{avg_rating || 'No rating available'}</span>
        <br /><br />
      </div>
      <div className="reviews_grid">
        <div className="reviews_wrapper">
          <h3>Positive Reviews:</h3>
          <div id="positive-reviews">{renderReviews(positive_reviews, 'positive')}</div> {/* Rendering positive reviews */}
        </div>
        <div className="reviews_wrapper">
          <h3>Negative Reviews:</h3>
          <div id="negative-reviews">{renderReviews(negative_reviews, 'negative')}</div> {/* Rendering negative reviews */}
        </div>
      </div>
    </div>
  );
}

export default ReviewResults;
