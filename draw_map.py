import webbrowser

import folium

# create map object
myMap = folium.Map(location=[50.45, 30.523333], zoom_start=10)

# add layers
folium.TileLayer('Stamen Terrain').add_to(myMap)
folium.TileLayer('Stamen Toner').add_to(myMap)
folium.TileLayer('Stamen Water Color').add_to(myMap)
folium.TileLayer('cartodbpositron').add_to(myMap)
folium.TileLayer('cartodbdark_matter').add_to(myMap)
folium.LayerControl().add_to(myMap)

# add markers to the map
folium.Marker(location=[50.455800, 30.563333], popup='Default popup Marker1', tooltip='Click here to see Popup').add_to(myMap)
folium.Marker(location=[50.475800, 30.723333], popup='<strong>Marker3</strong>', tooltip='<strong>Click here to see Popup</strong>').add_to(myMap)
folium.Marker(location=[50.465800, 30.503333], popup='<h3 style="color:green;">Marker2</h3>', tooltip='<strong>Click here to see Popup</strong>').add_to(myMap)
folium.Marker(location=[50.365800, 30.403333], popup='Custom Marker 3', tooltip='<strong>Click here to see Popup</strong>', icon=folium.Icon(color='purple', prefix='fa', icon='anchor')).add_to(myMap)

# draw map in browser
myMap.save('map.html')
webbrowser.open('map.html')
