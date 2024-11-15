function getReviews() {
    event.preventDefault(); 

    //Getting input values
    business_name = document.getElementById('business_name').value;
    location_name = document.getElementById('location').value; 

    //Making request to the webscraping and nlp api
    
}


review_btn = document.getElementById('review_btn');
review_btn.addEventListener("click", getReviews);
