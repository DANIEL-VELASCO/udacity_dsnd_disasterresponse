import sys
import pandas as pd
import numpy as np
import sqlite3
import re
import nltk
import pickle
import bz2
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()


def load_data(database_filepath):
    """This function loads the sqlite database"""    
    
    # load data from database
    conn = sqlite3.connect(database_filepath)
    cur = conn.cursor()
    df = pd.read_sql("SELECT * FROM real_life_disasters", con=conn)
    
    X = df[['message']].values.ravel()
    
    categories_list = ['related', 'request', 'offer', 'aid_related', 'medical_help', 'medical_products', 'search_and_rescue', 'security', 'military', 'child_alone', 'water', 'food', 'shelter', 'clothing', 'money', 'missing_people', 'refugees', 'death', 'other_aid', 'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods', 'storm', 'fire', 'earthquake', 'cold', 'other_weather', 'direct_report']
    
    Y = df[categories_list].values
        
    return X, Y, categories_list


def tokenize(text):
    """This function tokenize the text""" 
    
    # normalize case and remove punctuation
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())    
    # tokenize text
    tokens = word_tokenize(text)    
    # lemmatize andremove stop words
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return tokens



def build_model():
    """This function builds the pipeline of the ML model with TFIDF technique and multiouput random forest classifer along with grid search""" 
    
    pipeline = Pipeline([
        ('vect', CountVectorizer(lowercase=True,stop_words='english')),
        ('tfidf', TfidfTransformer()),
        ('multioutput_clf', MultiOutputClassifier(RandomForestClassifier(n_estimators=10)))
    ])

    parameters = {
        'vect__ngram_range': ((1, 1), (1, 2))  # unigrams or bigrams
    }
    
    # Grid search of hyperparameters
    cv = GridSearchCV(pipeline, param_grid=parameters)
    
    return cv #pipeline #cv
    

def evaluate_model(model, X_test, Y_test, category_names):
    """This function evaluate the model on the test set with f1, recall and precision metrics""" 
    
    # predict on test data
    y_pred_gridsearch = model.predict(X_test)

    df_metrics_gridsearch = pd.DataFrame()

    for column in range(36):

        
        precision = precision_score(Y_test[:,column], y_pred_gridsearch[:,column], average='weighted')
        recall = recall_score(Y_test[:,column], y_pred_gridsearch[:,column], average='weighted')
        f1 = f1_score(Y_test[:,column], y_pred_gridsearch[:,column], average='weighted')

        df_metrics_gridsearch.loc[column, 'category'] = category_names[column]
        df_metrics_gridsearch.loc[column, 'precision_cv'] = precision
        df_metrics_gridsearch.loc[column, 'recall_cv'] = recall
        df_metrics_gridsearch.loc[column, 'f1_cv'] = f1
        
        print('Category: {} -> precision: {}, recall: {}, f1: {}'.format(category_names[column],precision, recall, f1))
    
    return df_metrics_gridsearch
    
def save_model(model, model_filepath):
    """This function saves the model into a pkl file""" 
    
    #pickle.dump(model, open(model_filepath, 'wb'))

    ofile = bz2.BZ2File(model_filepath,'wb')
    pickle.dump(model,ofile)
    ofile.close()


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()