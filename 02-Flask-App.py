from flask import Flask, render_template, redirect, url_for,session,request,jsonify
from flask_wtf import FlaskForm
from explain import shaply
import pickle
#from threader import ThreadWithResult
import pandas as pd
import numpy as np
import time
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
from Database.Database import Connector

pkl_encoder = "Models/encoder.pickle"
with open(pkl_encoder, 'rb') as file1:
    oe = pickle.load(file1)
pkl_model="Models/best_model.pickle"
with open(pkl_model,'rb') as file2:
    model=pickle.load(file2)
pkl_scaler = "Models/scaler.pickle"
with open(pkl_scaler, 'rb') as file3:
    scaler = pickle.load(file3)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'




# http://wtforms.readthedocs.io/en/stable/fields.html
class InfoForm(FlaskForm):
    '''
    This general class to accept form data
    '''

    Item_weight = StringField('Item Weight (in kgs) :', validators=[DataRequired()],render_kw={"placeholder": "Item Weight(kgs)"})

    Item_visibility = StringField('Item Visibility :', validators=[DataRequired()],render_kw={"placeholder": "(Between 0-1)"})

    Item_mrp = StringField('Item MRP (in Rs) :', validators=[DataRequired()], render_kw={"placeholder": "Item Price"})

    Item_Identifier = SelectField('Choose the right Identifier  :', choices=list(oe.mapping[0]['mapping'][:-1].index))

    Item_Fat_Content = RadioField('Fat Contenet in the Item  :', choices=list(oe.mapping[1]['mapping'][:-1].index))

    Item_Type = SelectField('Item Type :', choices=list(oe.mapping[2]['mapping'][:-1].index))

    Year=SelectField('In which year was Outlet Built:',choices=list(oe.mapping[7]['mapping'][:-1].index))

    Outlet_Identifier = SelectField(' Outlet Identifier  :', choices=list(oe.mapping[3]['mapping'][:-1].index))

    Outlet_Size = RadioField('Size of the Outlet  :', choices=list(oe.mapping[4]['mapping'][:-1].index))

    Outlet_Location_Type = RadioField('Outlet Location Type :', choices=list(oe.mapping[5]['mapping'][:-1].index))

    Outlet_Type = RadioField('Outlet Type  :', choices=list(oe.mapping[6]['mapping'][:-1].index))

    submit = SubmitField('Submit')


def model_interpretability(model,content):

    """For calculating shap values """
    columns=['Item_Identifier','Item_Weight','Item_Fat_Content',
             'Item_Visibility','Item_Type',
             'Item_MRP','Outlet_Identifier','Outlet_Size',
             'Outlet_Location_Type','Outlet_Type','Year']
    column_mapping = {'Item_MRP': 'Price of the Item', 'Item_Fat_Content': 'Amount of Fat Content',
                      'Item_Identifier': 'Identifiers for certain Items',
                      'Item_Visibility': 'Total Visibility of that item in store',
                      'Item_Weight': 'Total weight of item', 'Item_Type': 'Type of Item',
                      'Year': 'Year in which outlet was built',
                      'Outlet_Identifier': 'Unique identifiers for Outlets', 'Outlet_Size': 'Size of the Outlet',
                      'Outlet_Type': 'Type of outlet', 'Outlet_Location_Type': 'Location of the Outlet'}
    interpretability=shaply(model)
    pos,neg=interpretability.get_shap_values(content,columns)
    pos_features=[column_mapping[fea] for fea in pos.keys() ]
    neg_features=[column_mapping[fea] for fea in neg.keys()]
    return pos_features,neg_features



def return_prediction(model,scaler,encoder,sample_json):
    
    # For larger data features, you should probably write a for loop
    # That builds out this array for you

    iw = sample_json['iw']
    iv = sample_json['iv']
    mrp= sample_json['mrp']
    ii = sample_json['ii']
    ifc = sample_json['ifc']
    it = sample_json['it']
    oi = sample_json['oi']
    os = sample_json['os']
    olt = sample_json['olt']
    ot = sample_json['ot']
    y=sample_json['y']

    iw=round(float(iw))
    mrp=round(float(mrp))
    columns=['Item_Identifier','Item_Weight','Item_Fat_Content','Item_Visibility','Item_Type','Item_MRP','Outlet_Identifier','Outlet_Size','Outlet_Location_Type','Outlet_Type','Year']

    nums=['Item_Weight','Item_Visibility','Item_MRP']
    pred_array= [[ii,iw,ifc,iv,it,mrp,oi,os,olt,ot,y]]
    pred_df = pd.DataFrame(pred_array, columns=columns)
    load_data = Connector()
    try:
        load_data.master()
        load_data.addData(pred_df)
    except:
        load_data.addData(pred_df)



    transformed_pred_df = encoder.transform(pred_df)
    transformed_pred_df[nums]=scaler.transform(transformed_pred_df[nums])



    #print(transformed_pred_df)

    training_data = "data_files/Train.csv"

    df = pd.read_csv(training_data)

    avg_sales= round(df[df['Item_Type'] == it]['Item_Outlet_Sales'].mean(),2)

    value = model.predict(transformed_pred_df)

    value=value[0]

    value=np.round(value,2)

    return value,transformed_pred_df,avg_sales

@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = InfoForm()
    # If the form is valid on submission 
    if form.validate_on_submit():

        # Grab the data from  form.

        session['Item_weight'] = form.Item_weight.data
        session['Item_visibility'] = form.Item_visibility.data
        session['Item_mrp'] = form.Item_mrp.data
        session['Item_Identifier'] = form.Item_Identifier.data
        session['Item_Fat_Content'] = form.Item_Fat_Content.data
        session['Item_Type'] = form.Item_Type.data
        session['Outlet_Identifier'] = form.Outlet_Identifier.data
        session['Outlet_Size'] = form.Outlet_Size.data
        session['Outlet_Location_Type'] = form.Outlet_Location_Type.data
        session['Outlet_Type'] = form.Outlet_Type.data
        session['Year']=form.Year.data


        return redirect(url_for("prediction"))


    return render_template('home.html', form=form)


@app.route('/prediction')
def prediction():

    #start=time.time()
    content = {}

    content['iw'] = session['Item_weight']
    content['iv'] = session['Item_visibility']
    content['mrp'] = session['Item_mrp']
    content['ii'] = session['Item_Identifier']
    content['ifc'] = session['Item_Fat_Content']
    content['it'] = session['Item_Type']
    content['oi'] = session['Outlet_Identifier']
    content['os'] = session['Outlet_Size']
    content['olt'] = session['Outlet_Location_Type']
    content['ot'] = session['Outlet_Type']
    content['y']=session['Year']

    print("[INFO] WEB Request  - ", content)

    preds,df,avg_sales = return_prediction(model=model, scaler=scaler, encoder=oe, sample_json=content)
    pos_features,neg_features=model_interpretability(model,df)
    print(pos_features,neg_features)



    #end=time.time()
    #total_time=end-start

    return render_template('thankyou.html', results=preds,item_type=content['it'],loc=content['ot'],pos=pos_features,neg=neg_features,avg_sales=avg_sales)


@app.route('/api/prediction', methods=['POST'])
def predict_flower():
    # RECIEVE THE REQUEST
    content = request.json

    # PRINT THE DATA PRESENT IN THE REQUEST
    print("[INFO] API Request - ", content)

    # PREDICT THE CLASS USING HELPER FUNCTION
    results = return_prediction(model=model, scaler=scaler,encoder=oe,sample_json=content)

    # PRINT THE RESULT
    print("[INFO] API Responce - ", results)

    # SEND THE RESULT AS JSON OBJECT
    return jsonify(results)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)