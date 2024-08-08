from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import pickle

def train_model(crop_id, seed_type):
    global model
    # Load and filter data
    data = pd.read_csv('csvfiles/test_act_weight_scores.csv')
    filtered_data = data[data['crop_id'] == crop_id]
    filtered_data = filtered_data[filtered_data['seed_type'] == seed_type]
    filtered_data = filtered_data.drop(['total_weightage', 'cmpl_total_weightage', 'primary_output'], axis=1)
    
    # Train the model
    X = filtered_data[['weight_score']]
    y = filtered_data['yield_per_acre']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Save the model
    pickle.dump(model, open("model.pkl", "wb"))

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)