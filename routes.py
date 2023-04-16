from flask import Flask, request, render_template
from form import ReusableForm
import json
import plotly
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas

app = Flask(__name__)

# prediction
@app.route("/", methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)

    if request.method == 'POST' and form.validate():
        # Extract from form
        year = request.form.getlist('year')
        time = request.form.getlist('time')
        print(year)
        print(time)
        new_df = crime_df.copy()

        new_df = new_df[new_df['DATE'].str.contains('|'.join(year)).any(level=0)]
        new_df = new_df[new_df['TIME'].str.contains('|'.join(time)).any(level=0)]

        fig = px.scatter_mapbox(new_df, lat="LATITUDE", lon="LONGITUDE", color="CATEGORY", opacity=0.75, size_max = 100, hover_data=["DATE", "TIME"],\
                                mapbox_style='open-street-map')
    else:
        fig = px.scatter_mapbox(crime_df, lat="LATITUDE", lon="LONGITUDE", color="CATEGORY", opacity=0.75, size_max = 100, hover_data=["DATE", "TIME"],\
                                mapbox_style='open-street-map')
    with open("limitespdq.geojson") as geojson:
        districts = json.load(geojson)
        gdf = geopandas.GeoDataFrame.from_features(districts)
        fig.update_layout(mapbox={"style": "open-street-map", "zoom": 10,\
                                "layers": [{"source": json.loads(gdf.geometry.to_json()), "below": "traces",\
                                            "type": "line", "color": "black", "line": {"width": 2.5},}]}, height=1000)
    fig.update_traces(marker={'size': 25})
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', form=form, graphJSON=graphJSON)

if __name__ == "__main__":
    crime_df = pd.read_csv('actes-criminels.csv')
    print("Successfully imported dataset")
    # crime_df['SIZE'] = pd.Series([1 for i in range(len(crime_df.index))])
    crime_df = crime_df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
    crime_df = crime_df[crime_df['LATITUDE'].notna()]
    crime_df = crime_df[crime_df['LONGITUDE'].notna()]
    crime_df = crime_df.replace({"CATEGORIE": {"Introduction": "Breaking and entering",\
                                           "Vol de véhicule à moteur": "Theft of a motor vehicle",\
                                           "Vol dans / sur véhicule à moteur": "Theft from/to a motor vehicle",\
                                          "Méfait": "Mischief", "Vols qualifiés": "Robbery",\
                                          "Infractions entrainant la mort": "Murder resulting in death"},\
                             "QUART": {"jour": "Day (8:01 a.m. to 4:00 p.m.)", "soir": "Evening (4:01 p.m. to midnight)",\
                                      "nuit": "Night (Midnight to 8:00 a.m.)"}})
    crime_df = crime_df.rename(columns={"CATEGORIE": "CATEGORY", "QUART": "TIME"})
    
    app.run(host="0.0.0.0", port=3000)