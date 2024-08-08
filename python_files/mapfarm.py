import sys
import plotly.express as px
import pandas as pd
import json

def generate_map(company_id, user_id):
    data2 = pd.read_csv('csvfiles/farms2.csv')
    
    # Drop rows where latitude and longitude are 0
    data2 = data2[(data2['latitude'] != 0) & (data2['longitude'] != 0)]
    
    # Filter by company_id
    if company_id != 0:
        data2 = data2[data2['company_id'] == company_id]
    
    if user_id != 0:
        # Filter by user_id if user_id is not 0
        data2 = data2[data2['user_id'] == user_id]

    # Ensure latitude and longitude are numeric
    data2['latitude'] = pd.to_numeric(data2['latitude'], errors='coerce')
    data2['longitude'] = pd.to_numeric(data2['longitude'], errors='coerce')

    # Drop rows with NaN values (resulting from conversion errors)
    data2 = data2.dropna(subset=['latitude', 'longitude'])

    # Enforce geographical boundaries of India
    min_lat_india, max_lat_india = 6.55, 37.09
    min_lon_india, max_lon_india = 68.11, 97.39

    data2 = data2[
        (data2['latitude'] >= min_lat_india) & (data2['latitude'] <= max_lat_india) &
        (data2['longitude'] >= min_lon_india) & (data2['longitude'] <= max_lon_india)
    ]

    # Load the GeoJSON file for India's states
    with open('csvfiles/india_state_geo.json') as f:
        india_states = json.load(f)

    if user_id != 0:
        # Calculate bounds if filtering by user_id
        min_lat = data2['latitude'].min()
        max_lat = data2['latitude'].max()
        min_lon = data2['longitude'].min()
        max_lon = data2['longitude'].max()

        # Calculate the center of the map
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2

        # Calculate zoom level
        lat_range = max_lat - min_lat
        lon_range = max_lon - min_lon
        zoom = 3.5  # Default zoom level
        if lat_range > 0 and lon_range > 0:
            zoom = 8 - max(lat_range, lon_range) * 0.5
    else:
        # Default center and zoom if not filtering by user_id
        center_lat = 23
        center_lon = 82
        zoom = 3.5

    # Create the bubble map
    fig3 = px.scatter_mapbox(
        data2,
        lat='latitude',
        lon='longitude',
        size='farm_area',
        color='user_name',
        hover_name='farm_name',
        mapbox_style="carto-positron",
        center={"lat": center_lat, "lon": center_lon},
        zoom=zoom
    )

    # Add the GeoJSON layer for India states
    fig3.update_layout(
        mapbox={
            'layers': [{
                'source': india_states,
                'type': 'line',
                'below': 'traces',
                'color': 'black',
                'line': {'width': 1},
            }]
        },
        title="Farm Locations in India",
        title_x=0.5,  # Center the title
        # height=700,  # Fixed height of the map
        # width=1000   # Fixed width of the map
    )

    fig3.write_html("./templates/fig3.html")
    print("map ran!")

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python3 map_plot.py <company_id> <user_id>")
#         sys.exit(1)

#     company_id = int(sys.argv[1])
#     user_id = int(sys.argv[2])
#     generate_map(company_id, user_id)
