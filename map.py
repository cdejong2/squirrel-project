import plotly.express as px
import geopandas as gpd
import pandas as pd
from sodapy import Socrata

def createMap():
    with Socrata("data.cityofnewyork.us", None) as client:
        results = client.get("vfnx-vebw", limit=2000)
        # Convert to pandas DataFrame
        squirrels = pd.DataFrame.from_records(results)


    points = squirrels['geocoded_column']
    #print(points[1]['coordinates'][1])
    df = pd.DataFrame(columns=['x', 'y'])

    for point in points:
        df.loc[len(df.index)] = [float(point['coordinates'][0]), float(point['coordinates'][1])]
    # ycolumn = squirrels.y()
    #print(df)

    px.set_mapbox_access_token('pk.eyJ1IjoiY2Rlam9uZzIiLCJhIjoiY2tyZG9mbmN3NWVkNDMwcnU2N202Z2pzdiJ9.wi9xk04T5EsRZ6i2XGfIZg')
    fig = px.scatter_mapbox(df,
                            lat='y',
                            lon='x',
                            zoom=14)
    fig.write_html('static/example.html')
    
createMap()

