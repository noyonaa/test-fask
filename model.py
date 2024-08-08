import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import linregress
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle

data = pd.read_csv('../csvFiles/act_weight_scores.csv')

filtered_data = data[data['crop_id'] == 885]

filtered_data = filtered_data.drop(['total_weightage', 'cmpl_total_weightage', 'primary_output'], axis=1)

correlation = filtered_data['weight_score'].corr(filtered_data['yield_per_acre'])

filtered_data['correlation'] = correlation

fig = px.scatter(filtered_data, x='weight_score', y='yield_per_acre', 
                 title=f'Yield per Acre vs Weight Score (Correlation: {correlation:.2f})')

slope, intercept, r_value, p_value, std_err = linregress(filtered_data['weight_score'], filtered_data['yield_per_acre'])
trendline = slope * filtered_data['weight_score'] + intercept

fig.add_trace(go.Scatter(
    x=filtered_data['weight_score'],
    y=trendline,
    mode='lines',
    name='Trendline'
))

fig.show()

X = filtered_data[['weight_score']]
y = filtered_data['yield_per_acre']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

weight_score_input = float(input("Enter a weight score: "))

predicted_yield = model.predict([[weight_score_input]])

pickle.dump(model, open("flask_app/model.pkl","wb"))

