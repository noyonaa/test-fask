import sys
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def yield_plot(crop_id):
   dataMA = pd.read_csv("csvfiles\\compliance.csv")
   dataMA['total'] =(dataMA['completed_activities'] + dataMA['completed_activities_with_p_remarks'])
   dataMA['compliance'] =(dataMA['total'] / dataMA['total_activities'])*100
   filtered_data = dataMA[dataMA['crop_id'] == crop_id]


    # Create scatter plot with trendline using Plotly Express
   fig = px.scatter(filtered_data, x="compliance", y="yield_per_area", trendline="ols", 
                    trendline_color_override="red", # Optional: Customize trendline color
                    title=f"Compliance vs Yield")

   fig.update_layout(
        xaxis_title='Compliance %',
        yaxis_title='Yield per unit area',
        height=500,  
        width=1100   
    )
   fig.write_html("htmls/fig1.html")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 companyplans.py <crop_id>")
        sys.exit(1)

    crop_id = int(sys.argv[1])
    yield_plot(crop_id)