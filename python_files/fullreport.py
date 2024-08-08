# import sys
# import pandas as pd

# def filter_and_analyze(plan_id, stage):
#     # Load data
#     data = pd.read_csv('csvfiles/plan_acts_dates.csv')
#     weather_data = pd.read_csv('csvfiles/weather.csv')
#     obs_data = pd.read_csv('csvfiles/act_obs.csv')

#     # Filter data
#     category_codes = ['FOPD', 'SOPD', 'SDTR', 'SPTR', 'LDTR']
#     filtered_data = data[
#         (data['plan_id'] == plan_id) &
#         (data['display_stage'] == stage) 
#        # & (data['category_code'].isin(category_codes)) 
#     ]

#     # Check if filtered_data is empty
#     if filtered_data.empty:
#         print("No data available for the specified plan_id and stage.")
#         return

#     first_record = filtered_data.iloc[0]
#     stage_start = first_record['stage_start']
#     stage_end = first_record['stage_end']
#     district = first_record['district']
    
#     # Filter weather data between stage_start and stage_end
#     weather_data = weather_data[
#         (weather_data['date'] >= stage_start) &
#         (weather_data['date'] <= stage_end) &
#         (weather_data['state'] == district)
#     ]

#     obs_data = obs_data[
#         (obs_data['obs_date'] >= stage_start) &
#         (obs_data['obs_date'] <= stage_end) 
#     ]


#     # Drop unnecessary columns from filtered data
#     filtered_data = filtered_data.drop(['plan_activity_id', 'plan_id', 'crop_id', 'farm_id', 'activity_id', 'company_id', 'display_stage', 'crop_stage_id', 'user_id'], axis=1)
    
#     # Define criteria for timeliness based on start date
#     filtered_data['on_time_start'] = (filtered_data['start_date'] == filtered_data['start_date_plan'])
    
#     # Filter for delayed activities
#     delayed_activities = filtered_data[~filtered_data['on_time_start']][['activity_name', 'start_date', 'end_date', 'start_date_plan', 'end_date_plan']]
    
#     # Rename columns for better display
#     delayed_activities.columns = ['Activity Name', 'Recommended Start Date', 'Recommended End Date', 'Actual Start Date', 'Actual End Date']
#     #number of records in delayed_activities

#     delayed_activities_no = len(delayed_activities)
#     # Convert the delayed activities to HTML table or "None" if empty
#     if delayed_activities.empty:
#         delayed_activities_html = "<p>None</p>"
#     else:
#         delayed_activities_html = delayed_activities.to_html(index=False, escape=False)
    
#     # Filter for pest and disease data
#     pest_data = obs_data[(obs_data['plan_id'] == plan_id) & (obs_data['tag'] == 'Pest') & (obs_data['pnd_class'] == 'PEST')]
#     disease_data = obs_data[(obs_data['plan_id'] == plan_id) & (obs_data['tag'] == 'Pest') & (obs_data['pnd_class'] == 'DISEASE')]

#     # Get unique pest and disease names
#     pest_names = pest_data['action_desc'].unique()
#     disease_names = disease_data['action_desc'].unique()
    
#     # Convert pest and disease names to HTML lists or "None" if empty
#     if pest_names.size == 0:
#         pest_names_html = "<p>None</p>"
#     else:
#         pest_names_html = "<ul>" + "".join(f"<li>{pest}</li>" for pest in pest_names) + "</ul>"
    
#     if disease_names.size == 0:
#         disease_names_html = "<p>None</p>"
#     else:
#         disease_names_html = "<ul>" + "".join(f"<li>{disease}</li>" for disease in disease_names) + "</ul>"
    
#     # HTML structure for the report
#     html_report = f"""
#     <html>
#         <head>
#             <title>Delayed Activities and Pest/Disease Report</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     margin: 3vw;
#                 }}
#                 table {{
#                     width: 100%;
#                     border-collapse: collapse;
#                 }}
#                 th, td {{
#                     border: 1px solid #ddd;
#                     padding: 8px;
#                 }}
#                 th {{
#                     background-color: #f2f2f2;
#                     text-align: left;
#                 }}
#                 h1 {{
#                     color: #333;
#                 }}
#                 p {{
#                     line-height: 1.6;
#                 }}
#                 ul {{
#                     list-style-type: none;
#                     padding: 0;
#                 }}
#                 li {{
#                     background: #f2f2f2;
#                     margin: 5px 0;
#                     padding: 10px;
#                     border-radius: 4px;
#                 }}
#             </style>
#         </head>
#         <body>
#             <h2>Delayed Activities in this stage - {delayed_activities_no}</h2>
#             {delayed_activities_html}
#             <h2>Pests Occurred in this stage</h2>
#             {pest_names_html}
#             <h2>Diseases Occurred in this stage</h2>
#             {disease_names_html}
#         </body>
#     </html>
#     """
    
#     # Save the report to an HTML file
#     with open("htmls/report1.html", "w") as file:
#         file.write(html_report)

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python3 fullreport.py <plan_id> <stage>")
#         sys.exit(1)
    
#     plan_id = int(sys.argv[1])
#     stage = int(sys.argv[2])
#     filter_and_analyze(plan_id, stage)


#--------------------------------------------------------------------------------------------------------------------


import sys
import pandas as pd
import os
from groq import Groq

groq_key = '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'

def filter_and_analyze(plan_id, stage):
    # Load data
    data = pd.read_csv('csvfiles/plan_acts_dates.csv')
    weather_data = pd.read_csv('csvfiles/weather.csv')
    obs_data = pd.read_csv('csvfiles/act_obs.csv')
    print(weather_data.head())
    weather_data = weather_data.drop('precipitation_cm', axis = 1)
    
    # Filter data
    category_codes = ['FOPD', 'SOPD', 'SDTR', 'SPTR', 'LDTR']
    filtered_data = data[
        (data['plan_id'] == plan_id) &
        (data['display_stage'] == stage) &
        (data['category_code'].isin(category_codes)) 
    ]

    first_record = filtered_data.iloc[0]
    stage_start = first_record['stage_start']
    stage_end = first_record['stage_end']
    district = first_record['district']
    
    # Filter weather data between stage_start and stage_end
    #weather_data['date'] = pd.to_datetime(weather_data['date'])
    weather_data = weather_data[
        (weather_data['date'] >= stage_start) &
        (weather_data['date'] <= stage_end) &
        (weather_data['state'] == district)
    ]

    print(weather_data)
    
    
    filtered_data = filtered_data.drop(['plan_activity_id', 'plan_id', 'crop_id', 'farm_id', 'activity_id', 'company_id', 'display_stage', 'crop_stage_id', 'user_id'], axis=1)
    
    # Descriptive statistics
    desc_stats = filtered_data.describe()
    
    # Define criteria for timeliness based on start date
    filtered_data['on_time_start'] = (filtered_data['start_date'] == filtered_data['start_date_plan'])
    
    # Summarize the timeliness
    timeliness_summary = filtered_data['on_time_start'].value_counts()
    on_time_activities = filtered_data[filtered_data['on_time_start']][['activity_name', 'user_name', 'start_date', 'end_date', 'start_date_plan', 'end_date_plan']]
    not_on_time_activities = filtered_data[~filtered_data['on_time_start']][['activity_name', 'user_name', 'start_date', 'end_date', 'start_date_plan', 'end_date_plan']]
    
    # Create a description for Groq API
    description = f"""
    Descriptive statistics:
    {desc_stats}

    Timeliness summary based on start date:
    {timeliness_summary}
    activities started on time:
    {on_time_activities.head(5).to_string(index=False)}
    activities not started on time:
    {not_on_time_activities.head(5).to_string(index=False)}
    """
    
    # Setup Groq API client
    client = Groq(api_key=groq_key)
    
    # Create the prompt for Groq API
    prompt = f"""The following data is for a field officer and the pest and disease activities related done, 
    focusing on activities in crop stage {stage}. 
    Indicate which activities were delayed.
    Start_date and end_date were recommended dates and start_date_plan and end_date_plan were the actual dates the activities were done.
    Based on the following description and data summary, 
    provide factual inferences. Find relationships and write them. 
    Make it STRICTLY FACTUAL and short:\n\n{description}"""
    
    # Call the Groq API to generate inferences and insights
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an agriculture data analysis expert who is writing a report."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
    )
    
    inferences1 = chat_completion.choices[0].message.content
    
    # Analyze pest data
    merged_pest_data = pd.merge(weather_data, obs_data, left_on='date', right_on='obs_date', how='inner')
    pest_data = merged_pest_data[(merged_pest_data['tag'] == 'Pest') & (merged_pest_data['plan_id'] == plan_id) & (merged_pest_data['pnd_class'] == 'PEST')]
    disease_data = merged_pest_data[(merged_pest_data['tag'] == 'Pest') & (merged_pest_data['plan_id'] == plan_id) & (merged_pest_data['pnd_class'] == 'DISEASE')]
    pest_data_filter = pest_data.filter(['temp_celsius', 'humidity', 'precipitation_cm', 'observation_value'])
    disease_data_filter = disease_data.filter(['temp_celsius', 'humidity', 'precipitation_cm', 'observation_value'])
    correlations_pest = pest_data_filter.corr()
    correlations_disease = disease_data_filter.corr()
    
    # Create a description for Groq API including pest data
    description_with_pest = f"""
    Previous Inferences:
    {inferences1}

    pest and disease related activities:
    Pests: {pest_data.to_string(index=False)}
    Diseases: {disease_data.to_string(index=False)}

    Correlations between pest observation and weather conditions:
    {correlations_pest}

    Correlations between disease observation and weather conditions:
    {correlations_disease}
    """
    
    # Create the prompt for Groq API with pest data
    prompt_with_pest = f"""Based on the previous inferences and the following pest and disease data, 
    provide factual inferences on how completing the activities on time affect pests. 
    The action_name is the name of the pest or disease, mention those in the insights. 
    Additionally, provide factual inference on how specific weather conditions will affect the observation value of the pest or disease. 
    Note: do NOT mention any column names:
    {description_with_pest}.
    Number the answers.
    Name the pest or disease in the inference. If anything is NaN, do not include it.
    List pests and diseases that occured in that stage SEPARATELY titled "Pests occurred" and "Diseases occurred".
    Correlations should show their original values and in a percentage manner.
    Make it sctrictly factual and short.
    Make sure the answer is CORRECT"""
    
    # Call the Groq API to generate additional inferences and insights
    chat_completion_with_pest = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an agriculture data analysis expert who is writing a report."},
            {"role": "user", "content": prompt_with_pest}
        ],
        model="llama3-8b-8192",
    )
    
    inferences2 = chat_completion_with_pest.choices[0].message.content
    
    # Escape backslashes and replace newlines with <br> for HTML
    inferences1_html = inferences1.replace("\\", "\\\\").replace("\n", '<br>')
    inferences2_html = inferences2.replace("\\", "\\\\").replace("\n", '<br>')
    
    # HTML structure for the report
    html_report = f"""
    <html>
        <head>
            <title>Field Officer Detailed Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 3vw;
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
            <h1>Inferences Timeliness of Pest and Disease related activities</h1>
            <p>{inferences1_html}</p>
            <h1>Inferences from Pest Data</h1>
            <p>{inferences2_html}</p>
        </body>
    </html>
    """
    
    # Save the report to an HTML file
    with open("htmls/report1.html", "w") as file:
        file.write(html_report)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 fullreport.py <plan_id> <stage>")
        sys.exit(1)
    
    plan_id = int(sys.argv[1])
    stage = int(sys.argv[2])
    filter_and_analyze(plan_id, stage)


