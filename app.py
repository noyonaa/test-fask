from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import plotly.express as px
from flask import render_template 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import python_files.pie_plot as pie_plot
import python_files.mapfarm as mapfarm
import python_files.abndacts as abndacts
import python_files.acreage as acreage
import python_files.baseline as baseline
import python_files.cmplacts as cmplacts
import python_files.companyacts as companyacts
import python_files.companyplans as companyplans
import python_files.compareyield as compareyield
import python_files.cropsyieldarea as cropsyieldarea
import python_files.cropsyieldareacompany as cropsyieldareacompany
import python_files.fullreport as fullreport
import python_files.plan_report as plan_report
import python_files.planactivityanalysis as planactivityanalysis
import python_files.stage_plan_abnd as stage_plan_abnd
import python_files.weightage as weightage
import python_files.modeltrainer as modeltrainer
import pickle

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


CORS(app)  # Enable CORS for all routes


@app.route('/', methods=['GET'])
def home():
    return "Hello! Love, Flask"


@app.route('/pie_plot', methods=['POST'])
def run_pie_plot():
    data = request.get_json()
    args = data.get('args', [])
    company_id = int(args[0])
    print(args)
    try:
        pie_plot.pie_plot(company_id)
        return jsonify({'message': 'Script executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/map_plot', methods=['POST'])
def run_map_plot():
    data = request.get_json()
    company_id = int(data.get('company_id'))
    user_id = int(data.get('user_id'))

    print("co: ", company_id,"fo_id: ", user_id )
    try:
        mapfarm.generate_map(company_id, user_id)
        return jsonify({'message': 'Script executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/weight-py', methods=['POST'])
def run_weight_py():
    data = request.get_json()
    company_id = int(data.get('company_id'))

    print("co: ", company_id)
    try:
        weightage.filter_and_plot(company_id)
        return jsonify({'message': 'Script executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/acre-py', methods=['POST'])
def run_acre_py():
    data = request.get_json()
    company_id = int(data.get('company_id'))

    print("co: ", company_id)
    try:
        acreage.filter_and_plot(company_id)
        return jsonify({'message': 'Script executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/filter_csv', methods=['POST'])
def run_filter_csv():
    data = request.get_json()
    company_id = int(data.get('company_id'))
    print("co: ", company_id)
    try:
        companyplans.filter_and_plot(company_id)
        return jsonify({'message': 'Script executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/acts_filter', methods=['POST'])
def run_acts_filter():
    data = request.get_json()
    company_id = int(data.get('company_id'))
    print("co: ", company_id)
    try:
        companyacts.filter_and_plot(company_id)
        return jsonify({'message': 'Script executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/plan_acts', methods=['POST'])
def run_plan_acts():
    data = request.get_json()
    company_id = int(data.get('company_id'))
    user_id = int(data.get('user_id'))
    sort = int(data.get('sort'))

    print("co: ", company_id, user_id, sort)
    try:
        plan_report.filter_and_plot(company_id, user_id, sort)
        print("script ran")
        return jsonify({'message': 'Script executed successfully'})
    except Exception as e:
        # Log the error with detailed information
        import traceback
        error_message = str(e)
        error_traceback = traceback.format_exc()
        print(f"Error: {error_message}")
        print(f"Traceback: {error_traceback}")
        return jsonify({'error': error_message, 'traceback': error_traceback}), 500

#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------MACHINE LEARNING-----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

@app.route('/train_model', methods=['POST'])
def run_train_model():
    data = request.get_json()
    crop_id = int(data.get('crop_id'))
    seed_type = data.get('seed_type')
    print("co: ", crop_id, "seed: ", seed_type)
    try:
        modeltrainer.train_model(crop_id, seed_type)
        return jsonify({'message': 'Script executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_yield', methods=['POST'])
def predict_yield():
    est_yield_data = pd.read_csv('csvfiles/est_yield_crop.csv')
    
    data = request.get_json()
    weight_score = float(data.get('weight_score'))
    block_area = float(data.get('block_area'))
    seed_type = data.get('seed_type')
    crop_id = int(data.get('crop_id'))
    print(seed_type)
    est_yield_data = est_yield_data[est_yield_data['seed_type']==seed_type]
    est_yield_data = est_yield_data[est_yield_data['crop_id']==crop_id]

    # Load the model if it's not already loaded
    model = pickle.load(open("model.pkl", "rb"))

    if weight_score == 1:
        # If weight_score is 1, use the value_text_en from est_yield_data
        predicted_yield_peracre = est_yield_data['value_text_en'].values[0]
    else:
        # Otherwise, use the model to predict
        predicted_yield_peracre = model.predict([[weight_score]])[0]

    predicted_yield = predicted_yield_peracre * block_area

    return jsonify({'predicted_yield': predicted_yield})

#------------------------------------------------------------------------------------------------------------------
#------------------------------SERVING FIGURES AS HTML PAGES IN TEMPLATE-------------------------------------------
#------------------------------------------------------------------------------------------------------------------

@app.route("/result", methods=['GET']) 
def serve_result(): 
    message = "first figure loaded"
    return render_template('fig1.html',  
                           message=message) 

@app.route("/result2", methods=['GET']) 
def serve_result2(): 
    message = "first figure loaded"
    return render_template('fig2.html',  
                           message=message)

@app.route("/result3", methods=['GET']) 
def serve_result3(): 
    message = "first figure loaded"
    return render_template('fig3.html',  
                           message=message)



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5001)
    app.run(debug=True)

