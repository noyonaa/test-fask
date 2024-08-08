import sys
import pandas as pd
import plotly.graph_objects as go

def generate_interpretation(data):
    interpretations = []
    
    max_weight = data['total_farm_area'].max()
    min_weight = data['total_farm_area'].min()
    avg_weight = data['total_farm_area'].mean()
    
    max_weight_row = data[data['total_farm_area'] == max_weight].iloc[0]
    min_weight_row = data[data['total_farm_area'] == min_weight].iloc[0]
    
    interpretations.append(f"The highest total acreage is {max_weight:.2f}, achieved by {max_weight_row['user_name']}.")
    interpretations.append(f"The lowest total acreage is {min_weight:.2f}, achieved by {min_weight_row['user_name']}.")
    
    high_workload_users = data[data['total_farm_area'] > 168]['user_name'].tolist()
    low_workload_users = data[data['total_farm_area'] < 50]['user_name'].tolist()
    optimized_workload_users = data[(data['total_farm_area'] <= 168) & (data['total_farm_area'] >= 50)]['user_name'].tolist()
    
    if high_workload_users:
        high_workload_str = ', '.join(high_workload_users)
        interpretations.append(f"Field officers {high_workload_str} have high workload scores. It is recommended to decrease their acreage as the workload is too much.")
    
    if low_workload_users:
        low_workload_str = ', '.join(low_workload_users)
        interpretations.append(f"Field officers {low_workload_str} have low workload scores. It is recommended to assign more farms to them as the workload is too low.")
    
    if optimized_workload_users:
        optimized_workload_str = ', '.join(optimized_workload_users)
        interpretations.append(f"Field officers {optimized_workload_str} have optimized workload scores. They can take up more farms as they have available capacity.")
    
    return interpretations

def filter_and_plot(company_id):
    data = pd.read_csv("csvfiles/weightage.csv")
    data['number_of_plans'] = data['number_of_plans'].fillna(1)
    data['weight'] = (data['farm_count'] * data['number_of_plans'] * data['total_farm_area']) / 100
    data['acre_score'] = data['total_farm_area']
    
    # data = data[data['weight'] > 200]
    data.sort_values(by='total_farm_area', ascending=False, inplace=True)
    if company_id != 0:
        data = data[data['company_id'] == company_id]

    bar_trace = go.Bar(
        x=data['user_name'],
        y=data['total_farm_area'],
        name='Total Farm Area',
        marker=dict(color='blue'),
    )

    line_trace = go.Scatter(
        x=data['user_name'],
        y=data['total_farm_area'],
        name='Line',
        mode='lines+markers',
        marker=dict(color='red'),
        line=dict(color='red')
    )

    fig = go.Figure()
    fig.add_trace(bar_trace)
    fig.add_trace(line_trace)

    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=168,
        x1=len(data['user_name']) - 0.5,
        y1=168,
        line=dict(color="black", width=2)
    )

    fig.update_layout(
        title='Field officers with the highest scores (>100)',
        xaxis_title='Field officers',
        yaxis_title='Score',
        barmode='overlay',
        yaxis=dict(showgrid=True, zeroline=True),
        xaxis=dict(showgrid=False, zeroline=True),
        showlegend=False
    )

    fig.write_html("templates/fig5.html")

    interpretations = generate_interpretation(data)

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
                </tr>
    """
    
    for index, row in data.iterrows():
        html_report += f"""
        <tr>
            <td>{row['user_name']}</td>
            <td>{row['farm_count']} Farms</td>
            <td>{row['total_farm_area']} </td>
        </tr>
        """
    
    html_report += """
            </table>
            <h2>Interpretations</h2>
            <ul>
    """
    
    for interpretation in interpretations:
        html_report += f"<li>{interpretation}</li>"
    
    html_report += """
            </ul>
        </body>
    </html>
    """
    

    with open("templates/report3.html", "w") as file:
        file.write(html_report)

    print('acreage ran!')
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python3 companyplans.py <company_id>")
#         sys.exit(1)

#     company_code = int(sys.argv[1])
#     filter_and_plot(company_code)
