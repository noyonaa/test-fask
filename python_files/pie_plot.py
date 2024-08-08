import sys
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import json
  
def pie_plot(company_id):
    data = pd.read_csv("csvfiles\\weightage.csv")
    data2 = pd.read_csv('csvfiles\\farms2.csv')
    data2 = data2[(data2['latitude'] != 0) & (data2['longitude'] != 0)]
    data['average_area'] = (data['total_farm_area'] / data['farm_count']).round(3)
    # sort data 
    data = data.sort_values(by='average_area', ascending=False)
    data = data.sort_values(by='farm_count', ascending=False)
    print('blueeeeeeeee')
    if company_id == 0:
        fig = px.pie(data, values=data['farm_count'], names=data['user_name'], labels={'farm_count':'No. of farms', 'user_name':'Field Officer'})
        fig.update_traces(textposition='inside', textinfo='label',)
        fig.update_layout(title="Number of Farms per Field Officer")
        fig.write_html("templates/fig1.html")

        fig2 = px.pie(data, values=data['total_farm_area'], names=data['user_name'], labels={'farm_count':'No. of farms', 'user_name':'Field Officer'})
        fig2.update_traces(textposition='inside', textinfo='label',)
        fig2.update_layout(title="Total area of Farms managed per Field Officer")
        fig2.write_html("templates/fig2.html")

        html_report = """
        <html>
            <head>
                <title>Field Officer Report</title>
                <style>
                    table {
                        font-family: Arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                    }
                    th, td {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <table>
                    <tr>
                        <th>Field Officer Name</th>
                        <th>Number of farms </th>
                        <th>Total Area Managed (in Acres)</th>
                        <th>Average Area Managed (in Acres)</th>
                    </tr>
        """
        
        for index, row in data.iterrows():
            html_report += f"""
            <tr>
                <td>{row['user_name']}</td>
                <td>{row['farm_count']} Farms</td>
                <td>{row['total_farm_area']} </td>
                <td>{row['average_area']}</td>
            </tr>
            """
        
        html_report += """
                </table>
            </body>
        </html>
        """

        with open("templates/report1.html", "w") as file:
            file.write(html_report)
        
    else:
        data = data[data['company_id']==company_id]
       
        fig = px.pie(data, values=data['farm_count'], names=data['user_name'], labels={'farm_count':'No. of farms', 'user_name':'Field Officer'})
        fig.update_traces(textposition='inside', textinfo='label',)
        fig.update_layout(title="Number of Farms per Field Officer")
        fig.write_html("templates/fig1.html")

        fig2 = px.pie(data, values=data['total_farm_area'], names=data['user_name'], labels={'farm_count':'No. of farms', 'user_name':'Field Officer'})
        fig2.update_traces(textposition='inside', textinfo='label',)
        fig2.update_layout(title="Total area of Farms managed per Field Officer")
        fig2.write_html("templates/fig2.html")

        html_report = """
        <html>
            <head>
                <style>
                    table {
                        font-family: Arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                    }
                    th, td {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <table>
                    <tr>
                        <th>Field Officer Name</th>
                        <th>Number of farms</th>
                        <th>Total Area Managed (in Acres)</th>
                        <th>Average Area Managed (in Acres)</th>
                    </tr>
        """
        
        for index, row in data.iterrows():
            html_report += f"""
            <tr>
                <td>{row['user_name']}</td>
                <td>{row['farm_count']}</td>
                <td>{row['total_farm_area']}</td>
                <td>{row['average_area']}</td>
            </tr>
            """
            
        html_report += """
                </table>
            </body>
        </html>
        """

        with open("templates/report1.html", "w") as file:
            file.write(html_report)
    
        
