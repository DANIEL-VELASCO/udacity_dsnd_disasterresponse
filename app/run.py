import json
import plotly
from flask import Flask
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from flask import render_template, request, jsonify
import plotly.graph_objs as gobjects
import joblib
from plots import return_figures
from plots import load_data
import bz2
import pickle
#import sys
#sys.path.insert(1,'/app/models')
#sys.path.insert(1,'/home/workspace/web_app/models')
#from train_classifier import tokenize
from joblib import dump, load

app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

#load data
df = load_data()

# load model
#model = joblib.load("../models/classifier.pkl")
# load model
ifile = bz2.BZ2File("/app/models/classifier.pkl",'rb')
#ifile = bz2.BZ2File('/home/workspace/web_app/models/classifier.pkl','rb')
model = pickle.load(ifile)
#model = load(ifile)
ifile.close()

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    graphs = return_figures(df)
        
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


#def main():
#    app.run(host='0.0.0.0', port=3000, debug=True)

if __name__ == '__main__':
    main()