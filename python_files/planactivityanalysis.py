import sys
import pandas as pd
import os
from groq import Groq

groq_key = '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'

def filter_and_plot(plan_id, stage):
    data = pd.read_csv('csvfiles/plan_acts_dates.csv')
    filtered_data = data[(data['plan_id'] == plan_id) & (data['display_stage'] == stage)]

    # Descriptive statistics
    desc_stats = filtered_data.describe()
    print(desc_stats)

    filtered_data = filtered_data.copy()
    # Define criteria for timeliness based on start date
    filtered_data.loc[:, 'on_time_start'] = (filtered_data['start_date'] == filtered_data['start_date_plan'])


    # Summarize the timeliness
    timeliness_summary = filtered_data['on_time_start'].value_counts()
    on_time_activities = filtered_data[filtered_data['on_time_start']][['activity_name', 'user_name', 'start_date', 'end_date', 'start_date_plan', 'end_date_plan']]
    not_on_time_activities = filtered_data[~filtered_data['on_time_start']][['activity_name', 'user_name', 'start_date', 'end_date', 'start_date_plan', 'end_date_plan']]

    # Create a description for Groq API
    description = f"""
    Descriptive statistics:
    {desc_stats.to_string()}

    Timeliness summary based on start date:
    {timeliness_summary.to_string()}

    activities started on time:
    {on_time_activities.head(5).to_string(index=False)}

    activities not started on time:
    {not_on_time_activities.head(5).to_string(index=False)}
    """

    # Setup Groq API client
    client = Groq(api_key=groq_key)

    # Create the prompt for Groq API
    prompt = (
        f"The following data is for one field officer only, focusing on activities in crop stage {stage}. "
        "The data includes information on activity name, user name, start date, end date, start date plan, "
        "and end date plan. Please provide insights and inferences based on this data."
        "start date plan is what was actually done and start date is what was recommended"
        "similarly end date plan is what was actually done and end date is what was recommended"
        "Comment on the field officer selected and his performance."
        "Indicate which activities did not start on time."
        "DO NOT PRINT THE DESCRIPTIVE STATISTICS, ONLY INFERENCE."
        "Make this inference in numbered points."
        f"{description}"
    )

    # Call the Groq API to generate inferences and insights
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an agriculture data analysis expert who is writing a report."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
    )

    inferences = chat_completion.choices[0].message.content
    # Escape backslashes and replace newlines with <br> for HTML
    inferences_html = inferences.replace("\\", "\\\\").replace("\n", '<br>')
    
    # HTML structure for the first report (filtered data)
    html_report_filtered = f"""
    <html>
        <head>
            <title>Field Officer Detailed Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                h1 {{
                    color: #333;
                }}
                p {{
                    line-height: 1.6;
                }}
            </style>
        </head>
        <body>
            <h1>Inferences</h1>
            <p>{inferences_html}</p>
        </body>
    </html>
    """
    
    # Save the filtered report to an HTML file
    with open("htmls/report1.html", "w") as file:
        file.write(html_report_filtered)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 planactivityanalysis.py <plan_id> <stage>")
        sys.exit(1)
    
    plan_id = int(sys.argv[1])
    stage = int(sys.argv[2])
    filter_and_plot(plan_id, stage)
