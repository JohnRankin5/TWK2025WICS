from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Recipe

# Create your views here.

def home(request):
    return render(request, "recipes/home.html")


def recipes(request):
    recipe_list = Recipe.objects.all()
    return render(request, "recipes/recipes.html", {"recipes": recipe_list})

def parking(request):
    return render(request, "recipes/parking.html")

import folium
import pandas as pd
import os
from django.shortcuts import render
from folium.plugins import HeatMap

# Ensure templates directory exists
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Load the dataset
file_path = file_path = r"C:\Users\jdrga\OneDrive\Desktop\TWK\WICS2025\Geocoded_Parking_Tickets.csv"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

geocoded_df = pd.read_csv(file_path)

# Drop rows with missing coordinates
geocoded_df = geocoded_df.dropna(subset=['Latitude', 'Longitude'])
geocoded_df['Latitude'] = geocoded_df['Latitude'].astype(float)
geocoded_df['Longitude'] = geocoded_df['Longitude'].astype(float)

def get_map():
    """ Generate a Folium map with heatmap and markers """
    
    # Define map center
    map_center = [geocoded_df['Latitude'].mean(), geocoded_df['Longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=12.5, tiles="cartodbpositron", control_scale=True)

    # Add red markers for ticket locations
    for _, row in geocoded_df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.8,
            popup=f"Tickets at this location"
        ).add_to(m)

    # Add heatmap layer
    heat_data = geocoded_df[['Latitude', 'Longitude']].values.tolist()
    if heat_data:
        HeatMap(heat_data, radius=20, blur=15, max_zoom=1).add_to(m)

    # Save map as HTML inside the `templates/` directory
    map_path = os.path.join(TEMPLATES_DIR, "map.html")
    m.save(map_path)
    return map_path

def map_view(request):
    """ Django view to render the map """
    get_map()  # Generate the map
    return render(request, "map.html")
