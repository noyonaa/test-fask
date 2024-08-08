import sys
import pandas as pd
import plotly.graph_objects as go

def filter_and_plot(company_code):
    # Load the data
    data1 = pd.read_csv("csvfiles\\plans_by_FO_companies.csv")

    data1['Total'] = data1["ABND_plans"] + data1["CMPL_plans"] + data1["PLAN_plans"] + data1["UNPL_plans"] + data1["WORK_plans"] + data1["HARV_plans"]
    data1['percent_cmpl'] = round((data1["CMPL_plans"] / data1['Total']) * 100, 2)
    data1['percent_abnd'] = round((data1["ABND_plans"] / data1['Total']) * 100, 2)
    data1['percent_plan'] = round((data1["PLAN_plans"] / data1['Total']) * 100, 2)
    data1['percent_unpl'] = round((data1["UNPL_plans"] / data1['Total']) * 100, 2)
    data1['percent_work'] = round((data1["WORK_plans"] / data1['Total']) * 100, 2)
    data1['percent_harv'] = round((data1["HARV_plans"] / data1['Total']) * 100, 2)

    data1.sort_values(by='percent_cmpl', ascending=True, inplace=True)
    data = data1[data1['company_id'] == company_code]
    

    fig = go.Figure([
        go.Bar(name='Completed Plans', x=data["percent_cmpl"], y=data["user_name"], marker_color='rgb(45, 198, 83)',orientation='h'),
        go.Bar(name='Abandoned Plans', x=data["percent_abnd"], y=data["user_name"], orientation='h')
    ])

    fig.update_layout(barmode='group', xaxis_title="Field Officer", yaxis_title="Percent Plans", title="Percentage of completed and abandoned Plans by FO against total", 
                      height=600,
        xaxis=dict(range=[0,100]))
    
    fig.write_html("templates/fig1.html")

    fig2 = go.Figure([
        go.Bar(name='Planned', x=data["PLAN_plans"], y=data["user_name"], orientation='h'),
        go.Bar(name='Unplanned', x=data["UNPL_plans"], y=data["user_name"], orientation='h'),
        go.Bar(name='Harvest', x=data["HARV_plans"], y=data["user_name"], orientation='h'),
        go.Bar(name='Work', x=data["WORK_plans"], y=data["user_name"], orientation='h'),
        go.Bar(name='Completed', x=data["CMPL_plans"], y=data["user_name"], orientation='h'),
        go.Bar(name='Abandoned', x=data["ABND_plans"], y=data["user_name"], orientation='h'),
    ])

    fig2.update_layout(barmode='group', xaxis_title="Field Officer", yaxis_title="Number of Plans", title="Number of Plans by FO", height=700)
    fig2.write_html("templates/fig2.html")

    fig3 = go.Figure([
        go.Bar(name='Planned', x=data["percent_plan"], y=data["user_name"], orientation='h', marker_color='#118ab2'),
        go.Bar(name='Unplanned', x=data["percent_unpl"], y=data["user_name"], orientation='h', marker_color='#edafb8'),
        go.Bar(name='Harvest', x=data["percent_harv"], y=data["user_name"], orientation='h', marker_color='#E9C46A'),
        go.Bar(name='Work', x=data["percent_work"], y=data["user_name"], orientation='h', marker_color='#415a77'),
        go.Bar(name='Completed', x=data["percent_cmpl"], y=data["user_name"], orientation='h', marker_color='#a7c957'),
        go.Bar(name='Abandoned', x=data["percent_abnd"], y=data["user_name"], orientation='h', marker_color='#d62828'),

    ])

    fig3.update_layout(barmode='group', xaxis_title="Field Officer", yaxis_title="Percent", title="Percentage plans by FO", height=700,xaxis=dict(range=[0,100]))
    fig3.write_html("templates/fig3.html")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 companyplans.py <company_id>")
        sys.exit(1)

    company_code = int(sys.argv[1])
    filter_and_plot(company_code)
