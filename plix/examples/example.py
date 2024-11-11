from plix import Slide,Presentation,Bibliography
import plotly.express as px
from plix import Slide
import geopandas as gpd

s1 = Slide().text('Plix: Storytelling with Interactive Data',y=0.75,color='#FFDAB9',\
               fontsize=0.08).\
               text('Giuseppe Romano',y=0.6,fontsize=0.04).\
                text('(Presentation made with Plix)',y=0.3,fontsize=0.04)
               #text('*Founder and CEO*',y=0.53,fontsize=0.04).\
              



df = px.data.election()

geo_df = gpd.GeoDataFrame.from_features(
    px.data.election_geojson()["features"]
).merge(df, on="district").set_index("district")

fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,
                           color="Joly",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="open-street-map",
                           zoom=8.5)

# Update colorbar text color
fig.update_coloraxes(colorbar=dict(
    title_font=dict(color='#DCDCDC'),  # Color of the colorbar title
    tickfont=dict(color='#DCDCDC')     # Color of the colorbar tick labels
))

# Update the background color of the whole plot
fig.update_layout(
    paper_bgcolor='#303030',  # Background color of the entire plot
    plot_bgcolor='#303030',   # Background color of the plot area
    font=dict(color='#DCDCDC')  # General font color for text elements
)




s2 = Slide().text('The problem',y=0.85,color='#FFDAB9',fontsize=0.08).\
             text('Data is dynamic but presentations are static',x=0.05,y=0.55,fontsize=0.05,w=0.4).\
             text('''For example, this map can't be zoomed in''',x=0.05,y=0.35,fontsize=0.05,w=0.3).\
             shape('arrow',x=0.34,y=0.29,w=0.1,orientation=0).\
             img('assets/map.png',x=0.45,y=0.25,w=0.5)


s3 = Slide().text('The solution: Plix',y=0.85,color='#FFDAB9',fontsize=0.08).\
             text('With Plix you can interact with data directly in the slide.',x=0.05,y=0.55,fontsize=0.05,w=0.4).\
             text('''Now you can zoom in''',x=0.05,y=0.35,fontsize=0.05,w=0.3).\
             text('''(if the map is misplaced refresh the page)''',x=0.05,y=0.05,fontsize=0.03,w=0.25,color='#FFDAB9').\
             shape('arrow',x=0.34,y=0.29,w=0.1,orientation=0).\
             plotly(fig,w=0.53,x=0.45,y=0.25)


df = px.data.iris()

fig = px.scatter(df, x="sepal_width", \
                      y="sepal_length", \
                      color="species")

s4 = Slide().\
     text('Example: Scatterplots',y=0.15,fontsize=0.05).\
     text('''(if the map is misplaced refresh the page)''',x=0.05,y=0.1,fontsize=0.03,w=0.3,color='#FFDAB9').\
     plotly(fig,w=0.7,y=0.25)

s5 = Slide().\
     text('Example: Molecules',y=0.85,fontsize=0.05).\
     text('(you can rotate it, zoom in etc...)',y=0.1,fontsize=0.05).\
     molecule('7R5N',w=0.7)

s6 = Slide().\
     text('Example: 3D models',y=0.15,fontsize=0.05).\
     model3D('assets/Blue_end.glb').text('Blue Flower Animated" (https://skfb.ly/oDIqT) by morphy.vision is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).',y=0.000,fontsize=0.03)

s7 = Slide().\
     text('Example: Python',y=0.85,fontsize=0.05).\
     python(w=0.7,y=0.1,h=0.7,x=0.15)


text = r'''
```Python
from plix import Slide

Slide().text('<u> This </u> **text** is *really important*.',\
               x=0.2,y=0.6,\
               fontsize=0.1,color='orange').show()
```
'''
s8 = Slide().\
     text('Technology',y=0.85,fontsize=0.08,color='#FFDAB9').\
     text('Plix combines the flexibility of Python with the rich visualization ecosystem of Javascript',y=0.65,fontsize=0.04).\
     text('Slides are created with Python and shared in the cloud',y=0.55,fontsize=0.04).\
     shape('arrow',x=0.5,y=0.25,w=0.07,orientation=0).\
     img('assets/example.png',x=0.6,y=0.15,w=0.3,frame=True).\
     text(text,y=0.17,fontsize=0.02,x=0.1)
     
     
               
#Presentation([s1,s2,s3,s4,s5,s6,s7,s8],title='pitch').show()


#dragon = Slide().\
#     text('Example: 3D models',y=0.15,fontsize=0.05).\
#     model3D('assets/dragon_gold.glb').text('Blue Flower Animated" (https://skfb.ly/oDIqT) by morphy.vision is licensed under Creative Commons Attribution (http://creativecommons.org/licenses/by/4.0/).',y=0.000,fontsize=0.03)

#Presentation([s6],title='test2').show()
Presentation([s6],title='test2').share()


