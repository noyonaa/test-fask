import sys
import pandas as pd
import plotly.graph_objects as go

def filter_and_plot(company_code):
    # Load the data
    data1 = pd.read_csv("csvfiles/all_activityplans_byName.csv")

    # Calculate total and percentages
    data1['Total'] = data1["ABND_act"] + data1["CMPL_act"] + data1["PLAN_act"] + data1["UNPL_act"]
    data1['percent_cmpl'] = round((data1["CMPL_act"] / data1['Total']) * 100, 2)
    data1['percent_abnd'] = round((data1["ABND_act"] / data1['Total']) * 100, 2)
    data1['percent_plan'] = round((data1["PLAN_act"] / data1['Total']) * 100, 2)
    data1['percent_unpl'] = round((data1["UNPL_act"] / data1['Total']) * 100, 2)
    data1.sort_values(by='percent_cmpl', ascending=False, inplace=True)

    # Filter data for the specified company
    data = data1[data1['company_id'] == company_code]

    # Plot 1: Percentage of completed and abandoned activities
    fig = go.Figure([
        go.Bar(name='Completed Activities', x=data["user_name"], y=data["percent_cmpl"], marker_color='rgb(45, 198, 83)'),
        go.Bar(name='Abandoned Activities', x=data["user_name"], y=data["percent_abnd"])
    ])

    fig.update_layout(barmode='group', xaxis_title="User Name", yaxis_title="Percent Activitites", 
                      title="Percentage of Completed and Abandoned Activities by FO Against Total", height=500)
    fig.write_html("templates/fig1.html")

    # Plot 2: Number of plan activities
    fig2 = go.Figure([
        go.Bar(name='Completed Activities', x=data["user_name"], y=data["CMPL_act"]),
        go.Bar(name='Abandoned Activities', x=data["user_name"], y=data["ABND_act"]),
        go.Bar(name='Planned Activities', x=data["user_name"], y=data["PLAN_act"]),
        go.Bar(name='Unplanned Activities', x=data["user_name"], y=data["UNPL_act"])
    ])

    fig2.update_layout(barmode='group', xaxis_title="User Name", yaxis_title="Number of Activitites", 
                       title="Number of Plan Activities by FO", height=500)
    fig2.write_html("templates/fig2.html")

    # Plot 3: Percentage plan activities
    fig3 = go.Figure([
        go.Bar(name='Completed Activities', x=data["user_name"], y=data["percent_cmpl"]),
        go.Bar(name='Abandoned Activities', x=data["user_name"], y=data["percent_abnd"]),
        go.Bar(name='Planned Activities', x=data["user_name"], y=data["percent_plan"]),
        go.Bar(name='Unplanned Activities', x=data["user_name"], y=data["percent_unpl"])
    ])

    fig3.update_layout(barmode='group', xaxis_title="User Name", yaxis_title="Percent Activities", 
                       title="Percentage Plan Activities by FO", height=500)
    fig3.write_html("templates/fig3.html")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 companyacts.py <company_id>")
        sys.exit(1)

    company_code = int(sys.argv[1])
    filter_and_plot(company_code)
