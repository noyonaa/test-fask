import sys
import pandas as pd
import plotly.express as px

def yield_plot(crop_id, company_id, user_id):
    # Load the data from the CSV file
    data = pd.read_csv("csvfiles/act_abnd.csv")
    
    # Filter data based on crop_id and company_id
    if crop_id != 0:
        data = data[data['crop_id'] == crop_id]
    if company_id != 0:
        data = data[data['company_id'] == company_id]

    # Calculate activity frequencies
    activity_counts = data['activity_name'].value_counts()

    # Get the top 10 activities for the histogram
    top_activities_histogram = activity_counts.head(10).index
    top_data_histogram = data[data['activity_name'].isin(top_activities_histogram)]
    
    # Generate the histogram sorted by activity frequency
    fig1 = px.histogram(top_data_histogram, x='activity_name', color='crop_name',
                        category_orders={"activity_name": top_activities_histogram},
                        title='Top 10 Abandoned Activities per Crop',
                        labels={'activity_name': 'Activity Name', 'crop_name': 'Crop Name'})
    
    # Rotate x-axis labels for better readability
    fig1.update_layout(xaxis_tickangle=-45) 
    #fig1.write_html(f"htmls/{user_id}/fig1.html")
    fig1.write_html(f"htmls/fig1.html")


    # Sort remarks by count in descending order
    remarks_order = top_data_histogram['remarks'].value_counts().index.tolist()

    # Generate the histogram with remarks stacked in descending order
    fig3 = px.histogram(top_data_histogram, x='activity_name', color='remarks_code',
                        category_orders={"activity_name": top_activities_histogram,},
                        title='Top 10 Abandoned Activities - coded by remarks',
                        labels={'activity_name': 'Activity Name', 'remarks': 'Reason'})
    
    # Rotate x-axis labels for better readability
    fig3.update_layout(xaxis_tickangle=-45)
    #fig3.write_html(f"htmls/{user_id}/fig3.html")
    fig3.write_html(f"htmls/fig3.html")
    

    # Sort activity counts and get the top 30 activities for the pie chart
    top_activities_pie = activity_counts.head(20).reset_index()
    top_activities_pie.columns = ['activity_name', 'count']
    
    # Generate the pie chart for top 30 activity frequencies
    fig2 = px.pie(top_activities_pie, values='count', names='activity_name', 
                  title='Top 20 Stage Wise Abandonment of Activities')
    fig2.update_traces(textposition='inside', textinfo='label')
    #fig2.write_html(f"htmls/{user_id}/fig2.html")
    fig2.write_html(f"htmls/fig2.html")

    # Determine the most abandoned activity
    most_abandoned_activity = activity_counts.idxmax()
    most_abandoned_activity_count = activity_counts.max()

    # Write the analysis to an HTML file
    analysis_html = f"""
    <html>
    <head><title>Activity Abandonment Analysis</title></head>
    <body>
        <h1>Activity Abandonment Analysis</h1>
        <p>The activity that is abandoned the most is <strong>{most_abandoned_activity}</strong> with a count of <strong>{most_abandoned_activity_count}</strong>.</p>
    </body>
    </html>
    """

    with open(f"htmls/report1.html", "w") as file:
        file.write(analysis_html)

    # with open(f"htmls/{user_id}/report1.html", "w") as file:
    #     file.write(analysis_html)

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python3 abndacts.py <crop_id> <company_id>")
#         sys.exit(1)

#     crop_id = int(sys.argv[1])
#     company_id = int(sys.argv[2])
#     user_id = int(sys.argv[3])
#     yield_plot(crop_id, company_id, user_id)
