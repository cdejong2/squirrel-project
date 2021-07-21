import plotly.express as px
import geopandas as gpd
import pandas as pd
from sodapy import Socrata
#from geojson import Feature, Point, FeatureColletion


with Socrata("data.cityofnewyork.us", None) as client:
    results = client.get("vfnx-vebw", limit=500)
    # Convert to pandas DataFrame
    squirrels = pd.DataFrame.from_records(results)


points = squirrels['geocoded_column']
print(points[1]['coordinates'][1])
df = pd.DataFrame(columns=['x', 'y'])
df.append(points[0]['coordinates'][0])
for point in points:
    df.append(point['coordinates'][0],point['coordinates'][1])
# ycolumn = squirrels.y()
    
#px.set_mapbox_access_token('pk.eyJ1IjoiY2Rlam9uZzIiLCJhIjoiY2tyZG9mbmN3NWVkNDMwcnU2N202Z2pzdiJ9.wi9xk04T5EsRZ6i2XGfIZg')
fig = px.scatter_mapbox(df,
                        lat=df.y,
                        lon=df.x,
                        hover_name="name",
                        zoom=1)
#fig.write_html('example.html')