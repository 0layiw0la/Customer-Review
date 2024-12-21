# Customer-Review Sentiment Analysis Web App

This project is a web app that uses sentiment analysis to enable users get the most recent positive and negative reviews for any business by putting in the name and location. 

- Web App link : [here](https://getcustomerreviews.netlify.app/)
- Docker hub repository : [here](https://hub.docker.com/r/0lay1w0la/customerreviewsapi)

**Features to be added:**
- direct link to instagram pages. 
- direct link to websites. 
- choose number of reviews. 
## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
  - [Backend API](#1-backend-api)
  - [Frontend](#2-frontend)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [API Endpoints](#api-endpoints)
  - [GET /](#get-)
  - [POST /get_reviews](#post-get_reviews)
- [Key Technologies](#key-technologies)
- [Deployment](#deployment)
  - [Backend (Azure Web App Service)](#backend-azure-web-app-service)
  - [Frontend (Netlify)](#frontend-netlify)
- [How It Works](#how-it-works)
- [Improvements and Roadmap](#improvements-and-roadmap)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Recent Reviews**: Focuses on the latest reviews for timely insights.
- **Sentiment Analysis**: Utilizes Natural Language Processing (NLP) to determine whether reviews are positive, negative, or neutral.
- **Interactive Interface**: Fully responsive web interface for seamless user experience.

## Architecture

The application is divided into two primary components:

### 1. **Backend API**
- Built using **FastAPI**.
- Incorporates **Selenium** for web scraping customer reviews from Google.
- Uses **NLTK Vader** for sentiment analysis.
- Packaged in a **Docker container** (hosted on Docker Hub) with **Chrome** and **ChromeDriver** pre-installed for web scraping functionality.
- Hosted on **Azure Web App Service**.

### 2. **Frontend**
- Developed with **React** (JavaScript, HTML, and CSS).
- Hosted on **Netlify** for a fast, reliable, and scalable frontend experience.

---

## Getting Started

### Prerequisites
Ensure the following tools are installed:
- **Docker**
- **Python 3.9+**
- **Node.js** (for frontend development)
- **Google Chrome** (optional for debugging Selenium locally)

### Setup Instructions

#### Backend
1. Clone the repository:
   ```bash
   git clone https://github.com/0layiw0la/Customer-Review.git
   cd customer-review/API
   ```
      
2. Build and run the Docker container:
   ```bash
   docker build -t customer-review-api .
   docker run -p 8000:8000 customer-review-api
   ```
   
    OR
   
1. Pull Docker image
    ```bash
    docker pull 0lay1w0la/customerreviewsapi
    ```
    
2. Run Docker container
   ```bash
   docker run -p 8000:8000 customer-review-api
   ```
   
#### Frontend
1. Navigate to the `Frontend` directory:
   ```bash
   cd ../Frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## API Endpoints
Api Link [here](https://customereeviewapp-bjdzasdpemesc4g0.canadacentral-01.azurewebsites.net)
### **GET /**
- **Description**: Test CORS setup.
- **Response**:
  ```json
  { "message": "cors works" }
  ```

### **POST /get_reviews**
- **Description**: Scrapes reviews for a given business and performs sentiment analysis.
- **Request Body**:
  ```json
  {  
    "business_name": "Example Business",  
    "location_name": "City, State"  
  }
  ```
- **Response**:
  ```json
  {  
    "positive_reviews": { "review1": "date1", "review2": "date2" },  
    "negative_reviews": { "review3": "date3", "review4": "date4" },  
    "avg_rating": 4.5  
  }
  ```

---

## Key Technologies
- **FastAPI**: For API development.
- **Selenium**: For web scraping reviews from Google.
- **NLTK Vader**: For sentiment polarity scoring.
- **Docker**: For containerization and easy deployment.
- **React**: For the frontend user interface.

---

## Deployment

### Backend (Azure Web App Service)
- The API is containerized and deployed using Azure's Web App Service. 
- The Docker image is hosted publicly on Docker Hub. [here](https://hub.docker.com/r/0lay1w0la/customerreviewsapi)

### Frontend (Netlify)
- The frontend is deployed on Netlify, ensuring fast and scalable delivery of the app.

---

## How It Works

1. **User Input**: Enter a business name and location.
2. **Web Scraping**: Backend scrapes Google reviews using Selenium.
3. **Sentiment Analysis**: Reviews are analyzed using NLTK Vader to classify them as positive, negative, or neutral.
4. **Results**: Displays the average rating, recent positive and negative reviews, and their dates.

---

## Improvements and Roadmap
- Expand review sources beyond Google.
- Add advanced filtering and categorization of reviews.
- Support for multiple languages.
- Upgrade hosting plan for more instances and faster response times.

---

## Contributing
Contributions are welcome! Please fork the repository, make changes, and submit a pull request.

---

## License
This project is licensed under the MIT License.


