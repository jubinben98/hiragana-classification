# Hiragana Letter Classification

This project contains a web front-end as a user interface where users can upload single or multiple images to view predictions. In the backend, it employs an Artificial Neural Network (ANN) classifier.

## Project Description

This repository presents a web application that serves as a user interface for Hiragana letter classification. Users can upload individual or multiple images containing Hiragana characters and subsequently receive predictions for each uploaded image. The project employs an ANN classifier to carry out the letter classification.

## Directory Structure Overview

- `Assignment`: Root directory.
  - `app/`: Main application module.
    - `static/`: Static assets directory.
      - `assets/`: Additional assets.
    - `templates/`: HTML templates directory.
      - `index.html`: Main page template.
      - `result.html`: Result page template.
    - `__init__.py`: Initialization script for the application module.
    - `routes.py`: Contains the route handlers.
    - `utils.py`: Utility functions.
    - `models/`: Directory for storing models.
      - `hiragana_classifier_v1.h5`: A pre-trained model.
    - `notebooks/`: Contains the notebook used for model training.
      - `Hiragana Classification.ipynb`: Notebook used to train the ANN model.
  - `run.py`: Script to run the Flask app.
  - `config.py`: Configuration settings.