import plotly.express as px
import pandas as pd
 
data = pd.read_csv("csvfiles\\stage_plan_abnd.csv")
 
data.sort_values(by='number', ascending=False, inplace=True)
data = data[data['crop_stage_id']!=9.0]
fig = px.pie(data, values='number', names='stage_name', title='Stage Wise Abandonment of plans')
fig.update_traces(textposition='inside', textinfo='label')

fig.write_html("htmls\\second.html")
