import plotly
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import plotly.graph_objs as gobjects
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()


def load_data():
    
    conn = sqlite3.connect('/app/data/DisasterResponse.db')
    cur = conn.cursor()
    df = pd.read_sql("SELECT * FROM real_life_disasters", con=conn)
    
    return df


def tokenize(text):    
    # normalize case and remove punctuation
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())    
    # tokenize text
    tokens = word_tokenize(text)    
    # lemmatize andremove stop words
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return tokens


def return_figures(df):
    
    # Chart 1: bar plot of the count of cases per category
    
    categories_list = ['related', 'request', 'offer', 'aid_related', 'medical_help', 'medical_products', 'search_and_rescue', 'security', 'military', 'child_alone', 'water', 'food', 'shelter', 'clothing', 'money', 'missing_people', 'refugees', 'death', 'other_aid', 'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods', 'storm', 'fire', 'earthquake', 'cold', 'other_weather', 'direct_report']

    cases_count = df[categories_list].sum()
    df_count_cases = pd.DataFrame({'category':cases_count.index, 'number_cases':cases_count.values}).sort_values(by='number_cases',ascending=False)    
    
    graph_1 = {
            'data': [
                gobjects.Bar(
                    x=df_count_cases['category'],
                    y=df_count_cases['number_cases']
                )
            ],

            'layout': {
                'title': 'Count of cases per category',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': ""
                }
            }
        }      
 

    # Chart 2: Top 20 of unigrams  
    def get_top_n_words(corpus, n=None):   
        vec = CountVectorizer(tokenizer=tokenize).fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
        return words_freq[:n]

    
    common_words = get_top_n_words(df['message'], 20)    
    df_common_words = pd.DataFrame(common_words, columns = ['words' , 'count'])    
    
    
    graph_2 = {
            'data': [
                gobjects.Bar(
                    x=df_common_words['words'],
                    y=df_common_words['count']
                )
            ],

            'layout': {
                'title': 'Top 20 unigrams',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': ""
                }
            }
        }

    graphs = []
    graphs.append(graph_1)
    graphs.append(graph_2)
    
    
    return graphs