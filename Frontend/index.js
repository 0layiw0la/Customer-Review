document.getElementById('review-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from reloading the page

    // Get input values
    const business_name = document.getElementById('business_name').value;
    const location_name = document.getElementById('location').value;

    // Get references to the review results div and the loading indicator
    const reviewResultsDiv = document.getElementById('review-results');
    

    // Hide the review results and show the loading indicator
    reviewResultsDiv.style.display = 'none'; // Hide results div while fetching
    

    // Make the API request to fetch reviews
    fetch('http://127.0.0.1:8000/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "business_name": business_name,
            "location_name": location_name
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);  // Show alert if there's an error
        } else {
            displayResults(data);
        }

        // Show the review results div
        reviewResultsDiv.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was an error fetching the reviews.");
    });
});

function displayResults(data) {
    // Get references to the result spans
    const positiveReviewSpan = document.getElementById('positive-reviews');
    const negativeReviewSpan = document.getElementById('negative-reviews');
    const avgRatingSpan = document.getElementById('avg-rating');

    // Display the average rating
    avgRatingSpan.innerHTML = data.avg_rating || 'No rating available';

    // Handle positive reviews
    let positiveReviews = data.positive_reviews;
    positiveReviewSpan.innerHTML = '';  // Clear previous results
    if (positiveReviews && typeof positiveReviews === 'object' && Object.keys(positiveReviews).length > 0) {
        Object.entries(positiveReviews).forEach(([review, date]) => {
            const reviewSpan = document.createElement('span');
            reviewSpan.classList.add('review');
            reviewSpan.innerHTML = `<div class="date"><i><b>${date}</i></b></div><div>${review}</div> `;
            positiveReviewSpan.appendChild(reviewSpan);
            positiveReviewSpan.appendChild(document.createElement('br'));  // Add a line break between reviews
        });
    } else {
        positiveReviewSpan.innerHTML = 'No positive reviews available.';
    }

    // Handle negative reviews
    let negativeReviews = data.negative_reviews;
    negativeReviewSpan.innerHTML = '';  // Clear previous results
    if (negativeReviews && typeof negativeReviews === 'object' && Object.keys(negativeReviews).length > 0) {
        Object.entries(negativeReviews).forEach(([review, date]) => {
            const reviewSpan = document.createElement('span');
            reviewSpan.classList.add('review');
            reviewSpan.innerHTML = `<div class="date"><i><b>${date}</i></b></div><div>${review}</div>`;
            negativeReviewSpan.appendChild(reviewSpan);
            negativeReviewSpan.appendChild(document.createElement('br'));  // Add a line break between reviews
        });
    } else {
        negativeReviewSpan.innerHTML = 'No negative reviews available.';
    }
}
