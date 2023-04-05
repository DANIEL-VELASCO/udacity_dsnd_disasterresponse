# Disaster Response Pipeline Project

## Table of Contents

1. Installation
2. How to run the notebook
3. Project Motivation
4. File Descriptions
5. Results
6. Licensing, Authors, and Acknowledgements


#### 1. Installation

In order to run the code you should count with the following libraries: json,plotly,flask, 
nltk, sklearn, pandas,sqlalchemy, sqlite3, pickle, re 

#### 2. How to run the notebook

1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Go to `app` directory: `cd app`
3. Run your web app: `python run.py`
4. Click the `PREVIEW` button to open the homepage

#### 3. Project Motivation

The purpose of this project is to create a machine learning model that allow to classify disaster messages and
that way send them to an appropriate disaster relief agency.

The full set of files were provided by figureeight company and they can be found in the data folder

### 4. File Descriptions

the app/run.py runs the web app and this file communicates with app/plots.py which contains the plots of the dashboard.
The templates of the web page are contained within the app/templates folder. In the data folder there is a script that read the provided
data, clean it (normalize text, remove stop words, execute a lemmatizer function and erase duplicated rows) and save it in a sqlite database.
In the models folder there is a "train_clasiffier.py" that creates the ML model to classify the messages and saves the model into a pkl file.

### 5. Results

A model that classify text messages was built and deployed into a web page. There are in total 36 different category dissasters and in general the metrics
of the test set (f1, precision and recall) showed a good performance. The top 20 of the most frequent unigrams showed key words which allow to classify messages.


### 6. Licensing, Authors, and Acknowledgements
Must give credit to figureeight for providing data and udacity instructors for their guidance and explanations.

