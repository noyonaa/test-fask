import sys
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def yield_plot(id1, id2, id3, id4, id5):
   data = pd.read_csv("csvfiles\\yield_totalArea.csv")
   data = data[(data['yield_per_area'] < 100000) & (data['yield_per_area'] > 0)]

   selected_crop_ids = [id1, id2, id3, id4, id5]

    # Filter the DataFrame for the selected crop IDs
   filtered_data = data[data['crop_id'].isin(selected_crop_ids)]

    # Create a box plot for the yield distribution of the selected crops
   fig = px.box(filtered_data,color='crop_name', y='yield_per_area', title='Yield Distribution for Selected Crops')

    # Show the plot
   fig.write_html("htmls/fig1.html")
   
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 companyplans.py <crop_id>")
        sys.exit(1)

    id1 = int(sys.argv[1])
    id2 = int(sys.argv[2])
    id3 = int(sys.argv[3])
    id4 = int(sys.argv[4])
    id5 = int(sys.argv[5])
    yield_plot(id1, id2, id3, id4, id5)