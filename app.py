import os
from flask import Flask, request, jsonify


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import requests
import json
import pandas as pd
from pprint import pprint
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

model = None
graph = None

# Loading a model with flask

def load_model():
    global model
    global graph
    model = pickle.load(open('predictingflightdelays.sav','rb'))


load_model()

def prepare_csv(filename):
    df=pd.read_csv(filename)
    return df.head()
    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    data = {"success": False}
    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file to the uploads folder
            file.save(filepath)

           

            # Convert data into csv file
            flight_data= prepare_csv(filepath)
            print(flight_data)

            

                # Use the model to make a prediction
            #for x in range(len(flight_data):
            
            predictions = []
 
            for x in range(len(flight_data)):
                predictions.append({'Record Number:': x+1,
                               'Value:': int(model.predict(flight_data)[x])})
            
            pprint(predictions)
                
            #flight_data["outcome"] = results

            # indicate that the request was a success
            # data["success"] = True

            #results_dict=results.to_dict('list')


            return jsonify(predictions) 
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value='Make Prediction'>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
