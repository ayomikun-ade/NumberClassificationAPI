# Number Classification API

A simple API built with Python and FastAPI that takes a number as input and returns interesting mathematical properties about it along with a fun fact from the Numbers API.

## Table of Contents

- [Features](#features)
- [API Specification](#api-specification)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Making Requests](#making-requests)
- [Deployment](#deployment)
- [License](#license)

## Features

- **Input Validation:** Returns a 400 error with a JSON error message for non-numeric inputs.
- **Mathematical Properties:**
  - Prime check
  - Perfect number check
  - Armstrong number check
  - Digit sum calculation
  - Parity ("even" or "odd") and "negative" property if applicable
- **Fun Fact:** Retrieves a math-related fun fact from [NumbersAPI](http://numbersapi.com).
- **CORS Support:** Handles Cross-Origin Resource Sharing using Gin's CORS middleware.
- **JSON Responses:** All responses are in JSON format.

## API Specification

### Endpoint

- **GET** `/api/classify-number?number=<your-number>`

### Success Response (200 OK)

Example for input `371`:

```json
{
  "number": 371,
  "is_prime": false,
  "is_perfect": false,
  "properties": ["armstrong", "odd"],
  "class_sum": 11,
  "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### Error Response (400 Bad Request)

Example for non-numeric input:

```json
{
  "number": "alphabet",
  "error": true
}
```

## Prerequisites

- [Python](https://python.org/) (version 3.10+ recommended)
- Git

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/ayomikun-ade/NumberClassifcationAPI.git
   cd NumberClassificationAPI
   ```

2. **Install Dependencies:**

   The project uses Python, FastAPI and its CORS middleware. Run:

   ```bash
   pip install fastapi pydantic requests uvicorn
   ```

   This command downloads the required dependencies for FastAPI and CORS middleware.

## Running the Application

To start the API server locally:

```bash
uvicorn main:app --reload
```

You should see a log message:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Making Requests

### Using cURL

```bash
curl "http://localhost:8080/api/classify-number?number=371"
```

### Using Postman

1. Set the request method to **GET**.
2. Enter the URL: `http://localhost:8080/api/classify-number?number=371`
3. Click **Send** and view the JSON response.

- **CORS:**  
  The API uses `cors` to allow all origins. Modify the configuration in `main.py` if needed.

**Ciao.**
