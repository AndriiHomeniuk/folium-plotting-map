import webbrowser

import folium

from coordinates.coordinates_for_path import *

m5 = folium.Map(location=[28.644800, 77.216721], tiles='cartodbpositron', zoom_start=14)


line_1 = folium.vector_layers.PolyLine(coords_1, popup='<b>Path of Vehicle_1</b>', tooltip='Vehicle_1', color='blue', weight=10)
line_2 = folium.vector_layers.PolyLine(coords_2, popup='<b>Path of Vehicle_2</b>', tooltip='Vehicle_2', color='red', weight=10)
line_3 = folium.vector_layers.PolyLine(coords_3, popup='<b>Path of Vehicle_3</b>', tooltip='Vehicle_3', color='green', weight=10)

line_1.add_to(m5)
line_2.add_to(m5)
line_3.add_to(m5)

folium.LayerControl().add_to(m5)

m5.save('map_india.html')
webbrowser.open('map_india.html')
