# Playoff Prediction Web App

This is a Flask web application that predicts playoff status for baseball teams based on various input features. It uses a trained Support Vector Classifier (SVC) model to make predictions.

## Features

- Predicts playoff status for baseball teams based on input data.
- Uses a PostgreSQL database to store input data and predictions.
- Allows users to input data through a web form and see the prediction result.

## Installation

To run this application locally, follow these steps:

1. Clone this repository:

   ```
   git clone https://github.com/SamerArkab/Playoffs_Prediction.git
   ```

2. Navigate to the repository directory:

   ```
   cd Playoffs_Prediction
   ```

3. Build and run the Docker containers using Docker Compose:

   ```
   docker-compose up --build
   ```

   This will start the PostgreSQL database and the Flask web application.

4. Access the web application in your browser at [http://localhost:5001](http://localhost:5001).

## Usage

1. Fill out the form on the web page with the required input data.
2. Click the "Predict" button to see the predicted playoff status.
3. The prediction result will be displayed on the page (and saved in the database).

## Development

To modify or extend this application, follow these guidelines:

- The Flask application logic is contained in `app.py`.
- The HTML templates for the web pages are in the `templates/` directory.
- Update the `requirements.txt` file with any additional Python dependencies.
- You can train a new model or modify the existing one in the `train_model.ipynb` notebook.
- Make sure to update the Dockerfile and Docker Compose configuration (`docker-compose.yml`) if you make changes to the application setup.

This project is licensed under the [MIT License](LICENSE).