import sys
import pandas as pd
import plotly.express as px
import warnings
import plotly.graph_objects as go 

# Suppress specific FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

def obs_plot(crop_id, company_id, farm_id, action_title):
    data = pd.read_csv("csvfiles\\act_obs.csv")
    data = data[data['tag'] == 'Pest']
    data = data[data['company_id'] == company_id]
    data = data[data['farm_id'] == farm_id]
    data = data[data['crop_id'] == crop_id]
    data['action_date'] = pd.to_datetime(data['action_date'])

    if (action_title!='all'):
        data = data[data['action_title'] == action_title]

    # Sort the DataFrame by action_date
    data = data.sort_values(by='action_date')


    if (action_title!='all'):
        fig = go.Figure()
        # Add the trace for observation_value
        fig.add_trace(go.Scatter(
            x=data['action_date'], 
            y=data['observation_value'], 
            mode='lines', 
            name='Observation Value',
            line=dict(shape='linear') ,
            
        ))
        fig.add_trace(go.Scatter(
            x=data['action_date'], 
            y=data['expected_value_min'], 
            mode='lines', 
            name='Expected Min Value',
            line=dict(dash='dot', shape='linear', color= '#d00000') 
        ))
        
        # Add the trace for expected_value_max
        fig.add_trace(go.Scatter(
            x=data['action_date'], 
            y=data['expected_value_max'], 
            mode='lines', 
            name='Expected Max Value',
            line=dict(dash='dot', shape='linear', color='#ff0000') 
        ))
        # Update the layout
        fig.update_layout(
            title='Pest and Disease Occurrence Through Time',
            xaxis_title='Date',
            yaxis_title='Severity %',
            legend_title='Legend',
            yaxis=dict(range=[0,100])
        )
        fig.write_html("htmls/fig1.html")

    else:

        # Create a time series plot
        fig = px.line(data, x='action_date', y='observation_value', color='action_desc', title='Pest and Disease Occurrence Through Time',
                    labels={'observation_value': 'Severity %', 'action_date': 'Date', 'action_desc': 'Pest/Disease'}, line_shape='linear',markers=True)
        fig.update_layout(
        yaxis=dict(range=[0,100])
        )
        # Show the plot
        fig.write_html("htmls/fig1.html")

        
        

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python pest-occurence.py <crop_id> <company_id> <farm_id>")
        sys.exit(1)

    crop_id = int(sys.argv[1])
    company_id = int(sys.argv[2])
    farm_id = int(sys.argv[3])
    action_title = sys.argv[4]
    obs_plot(crop_id, company_id, farm_id,action_title)
