import sys
import pandas as pd

def filter_and_plot(company_code, user_id, sort):
    # Load the data from CSV file
    data = pd.read_csv("csvfiles/plan_wise_activities.csv")
    
    # Filter the data for the specified company ID and user ID
    data = data[(data['company_id'] == company_code) & (data['modified_by'] == user_id) & (data['crop_id'] != 999)]
    
    # Initialize summary and other variables
    summary = pd.DataFrame()
    activity_column = ''
    activity_type = ''
    
    # Sorting criteria based on specified sort option
    if sort == 1:
        data = data.sort_values(by='CMPL_act', ascending=False)
        summary = data[data['CMPL_act'] > 0].groupby('crop_name').agg({'CMPL_act': 'sum'}).reset_index()
        activity_column = 'CMPL_act'
        activity_type = 'Completed Activities'
    elif sort == 2:
        data = data.sort_values(by='ABND_act', ascending=False)
        summary = data[data['ABND_act'] > 0].groupby('crop_name').agg({'ABND_act': 'sum'}).reset_index()
        activity_column = 'ABND_act'
        activity_type = 'Abandoned Activities'
    elif sort == 3:
        data = data.sort_values(by= 'PLAN_act', ascending=False)
        summary = data[data['PLAN_act'] > 0].groupby('crop_name').agg({'PLAN_act': 'sum'}).reset_index()
        activity_column = 'PLAN_act'
        activity_type = 'Planned Activities'
    elif sort == 4:
        data = data.sort_values(by='UNPL_act', ascending=False)
        summary = data[data['UNPL_act'] > 0].groupby('crop_name').agg({'UNPL_act': 'sum'}).reset_index()
        activity_column = 'UNPL_act'
        activity_type = 'Unplanned Activities'
    else:
        raise ValueError(f"Invalid sort value: {sort}")

    # Save the summary to CSV and JSON files
    summary.to_csv(f"csvfiles/summary.csv", index=False)
    summary.to_json(f"csvfiles/summary.json", orient='records')

    # HTML structure for the first report (filtered data)
    html_report_filtered = f"""
    <html>
        <head>
            <title>Field Officer Detailed Report</title>
            <style>
                table {{
                    font-family: Arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>Field Officer Detailed Report</h1>
            <table>
                <tr>
                    <th>Plan ID</th>
                    <th>Crop Name</th>
                    <th>Completed Activities</th>
                    <th>Abandoned Activities</th>
                    <th>Planned Activities</th>
                    <th>Unplanned Activities</th>
                </tr>
    """
    
    # Add rows for each plan in the filtered data
    for index, row in data.iterrows():
        html_report_filtered += f"""
        <tr>
            <td>{row['plan_id']}</td>
            <td>{row['crop_name']}</td>
            <td>{row['CMPL_act']}</td>
            <td>{row['ABND_act']}</td>
            <td>{row['PLAN_act']}</td>
            <td>{row['UNPL_act']}</td>
        </tr>
        """
    
    html_report_filtered += """
            </table>
        </body>
    </html>
    """
    
    # Save the filtered report to an HTML file
    with open("templates/report1.html", "w") as file:
        file.write(html_report_filtered)

    # HTML structure for the second report (summary data)
    html_report_summary = f"""
    <html>
        <head>
            <title>Summary: {activity_type}</title>
            <style>
                table {{
                    font-family: Arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h2>Summary: {activity_type}</h2>
            <table>
                <tr>
                    <th>Crop Name</th>
                    <th>Acts Number</th>
                </tr>
    """
    
    # Add rows for the summary data
    for index, row in summary.iterrows():
        html_report_summary += f"""
        <tr>
            <td>{row['crop_name']}</td>
            <td>{row[activity_column]}</td>
        </tr>
        """
    
    html_report_summary += """
            </table>
        </body>
    </html>
    """
    
    # Save the summary report to an HTML file
    with open("templates/report2.html", "w") as file:
        file.write(html_report_summary)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 plan_report.py <company_id> <user_id> <sort>")
        sys.exit(1)
    
    company_code = int(sys.argv[1])
    user_id = int(sys.argv[2])
    sort = int(sys.argv[3])
    filter_and_plot(company_code, user_id, sort)
