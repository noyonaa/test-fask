import sys
import pandas as pd
import plotly.express as px

def yield_plot(crop_id, company_id):
    data = pd.read_csv("csvfiles\\yield_totalArea.csv")
    # Filter data based on selected crop_id and company_id 
    filtered_data = data[(data['crop_id'] == crop_id) & (data['company_id'] == company_id) & (data['primary_output']<=100000)]
    # Create plot using Plotly Express
    fig = px.scatter(filtered_data, x="crop_area", y="yield_per_area", trendline="ols", 
                     trendline_color_override="green", title=f'Yield/Unit Area for Company ID {company_id}',hover_data=['primary_output'], color="state",
                     labels=dict(crop_area = "Given Area for crop", yield_per_area= "Yield per Unit area(kg)", primary_output= "Actual Yield(kg)", state= "State"))
    fig.update_layout(
        yaxis=dict(range=[0, filtered_data['yield_per_area'].max()*1.2]),
        xaxis=dict(range=[0, filtered_data['crop_area'].max()*1.2])
    )
    fig.write_html("htmls/fig1.html")

    fig2 = px.scatter(filtered_data, x="crop_area", y="primary_output", size=filtered_data['yield_per_area'], color = filtered_data['state'],
                      title=f'Bubble Chart- Total Yield vs Area {company_id}',
                      labels=dict(crop_area = "Given Area for crop", yield_per_area= "Yield per Unit area(kg)", primary_output= "Actual Yield(kg)", state= "State"))   
    fig2.update_layout(
        yaxis=dict(range=[0, filtered_data['primary_output'].max()*1.2]),
        xaxis=dict(range=[0, filtered_data['crop_area'].max()*1.2])
    )
    fig2.write_html("htmls/fig2.html")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 cropsyieldareacompany.py <crop_id> <company_id>")
        sys.exit(1)

    crop_id = int(sys.argv[1])
    company_id = int(sys.argv[2])
    yield_plot(crop_id, company_id)
