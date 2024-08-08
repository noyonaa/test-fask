import sys
import pandas as pd
import plotly.graph_objects as go

def generate_interpretation(data):
    interpretations = []
    
    # Overall statistics
    max_weight = data['weight'].max()
    min_weight = data['weight'].min()
    avg_weight = data['weight'].mean()
    
    max_weight_row = data[data['weight'] == max_weight].iloc[0]
    min_weight_row = data[data['weight'] == min_weight].iloc[0]
    
    interpretations.append(f"The highest workload score is {max_weight:.2f}, achieved by {max_weight_row['user_name']}.")
    interpretations.append(f"The lowest workload score is {min_weight:.2f}, achieved by {min_weight_row['user_name']}.")
    interpretations.append(f"The average workload score is {avg_weight:.2f}.")
    
    # Top 3 officers
    top_officers = data.head(3)
    for i, row in top_officers.iterrows():
        interpretations.append(f" {row['user_name']} has a workload score of {row['weight']:.2f}, "
                               f"managing {row['farm_count']} farms with {row['number_of_plans']} crop plans "
                               f"and a total farm area of {row['total_farm_area']} acres.")
    
    # Officers with high farm count but low weight
    high_farm_low_weight = data[(data['farm_count'] > 20) & (data['weight'] < avg_weight)]
    for i, row in high_farm_low_weight.iterrows():
        interpretations.append(f"{row['user_name']} manages a high number of farms ({row['farm_count']}) "
                               f"but has a lower workload score of {row['weight']:.2f}.")
    
    return interpretations

def filter_and_plot(company_code):
    data = pd.read_csv("csvfiles/weightage.csv")
    data['number_of_plans'] = data['number_of_plans'].fillna(1)
    data['weight'] = (data['farm_count'] * data['number_of_plans'] * data['total_farm_area']) / 100
    data = data[data['weight'] > 100]
    data.sort_values(by='weight', ascending=False, inplace=True)
    if company_code != 0:
        data = data[data['company_id'] == company_code]

    bar_trace = go.Bar(
        x=data['user_name'],
        y=data['weight'],
        name='Weight',
        marker=dict(color='blue'),
    )

    line_trace = go.Scatter(
        x=data['user_name'],
        y=data['weight'],
        name='Line',
        mode='lines+markers',
        marker=dict(color='red'),
        line=dict(color='red')
    )

    fig = go.Figure()
    fig.add_trace(bar_trace)
    fig.add_trace(line_trace)

    fig.update_layout(
        title=f'Field officers with the highest scores (>100)',
        xaxis_title='Field officers',
        yaxis_title='Score',
        barmode='overlay',
        yaxis=dict(showgrid=True, zeroline=True),
        xaxis=dict(showgrid=False, zeroline=True),
        showlegend=False
    )

    fig.write_html("templates/fig4.html")

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
                    <th>Number of Plans </th>
                    <th>Total Area Managed (in Acres)</th>
                    <th>Score</th>
                </tr>
    """
    
    for index, row in data.iterrows():
        html_report += f"""
        <tr>
            <td>{row['user_name']}</td>
            <td>{row['farm_count']} Farms</td>
            <td>{row['number_of_plans']}</td>
            <td>{row['total_farm_area']} </td>
            <td>{row['weight']}</td>
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

    print("weightage ran")

    with open("templates/report2.html", "w") as file:
        file.write(html_report)
