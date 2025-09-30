import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


file_path = "/content/sample_data/SF_Crashes.csv"
sfdata = pd.read_csv(file_path)

sfdata.head()


#heatmap using the lat and long variables to determine location density of crashes
from folium.plugins import HeatMap

data_geo = sfdata.dropna(subset=['tb_latitude', 'tb_longitude'])

m = folium.Map(location=[37.763439, -122.397710], zoom_start=10)  #San Francisco area

# heatmap
heat_data = [[row['tb_latitude'], row['tb_longitude']] for index, row in data_geo.iterrows()]
HeatMap(heat_data, radius=8, max_zoom=13).add_to(m)

m.save("SFHeatmap.html")

#TODO: Continue building your heatmap
# Sample a subset of the data for visualization
sample_data_severity = data_geo.sample(n=1000, random_state=42)

# Create a base map
m_severity = folium.Map(location=[37.763439, -122.397710], zoom_start=10)

#including severity in heatmap
for index, row in sample_data_severity.iterrows():
    if row['number_killed'] > 0:
        color = "RED"  # Fatalities

        folium.features.RegularPolygonMarker(
          location=[row['tb_latitude'], row['tb_longitude']],
          number_of_sides=3,
          radius=5,
          gradient = False,
          color=color,
          fill=True,
          fill_color=color
        ).add_to(m_severity)


    elif row['number_injured'] > 0:
        color = "PURPLE"  # Injuries
        folium.CircleMarker(
          location=[row['tb_latitude'], row['tb_longitude']],
          radius=5,
          color=color,
          fill=True,
          fill_color=color
       ).add_to(m_severity)
    else:
        color = "GRAY"  # relatively unscathed
        folium.features.RegularPolygonMarker(
          location=[row['tb_latitude'], row['tb_longitude']],
          number_of_sides=4,
          radius=5,
          gradient = False,
          color=color,
          fill=True,
          fill_color=color
        ).add_to(m_severity)


m_severity.save("SFseverity.html")
