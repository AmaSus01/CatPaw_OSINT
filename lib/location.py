import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from .local import *


def get_geolocation(place):
    geoTag = place
    geolocator = Nominatim(user_agent="GeoTag")
    location = geolocator.geocode(geoTag)
    if location is None:
        print(f"{fa}{re} Sorry but this place geoTag work incorrect")
        exit(1)
    else:
        print(f"{fa}{cy} If you want open map, press [Y/y]:", end='')
        x = input()
        if x == 'Y' or x == 'y':
            map_access_token = open(".mapbox_token").read()

            fig = go.Figure(go.Scattermapbox(
                lat=[location.latitude],
                lon=[location.longitude],
                mode='markers',
                marker=go.scattermapbox.Marker(size=16),
                text=['Approximate location'],
            ))

            fig.update_layout(
                hovermode='closest',
                mapbox=dict(
                    accesstoken=map_access_token,
                    bearing=0,
                    center=go.layout.mapbox.Center(
                        lat=int(location.latitude),
                        lon=int(location.longitude)
                    ),
                    pitch=0,
                    zoom=5
                )
            )
            fig.show()
        else:
            exit(1)