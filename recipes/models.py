from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.JSONField(
        default=list,
        help_text="List of ingredients as a JSON array (e.g., ['2 eggs', '1 cup sugar'])."
    )
    directions = models.JSONField(
        default=list,
        help_text="List of steps as JSON objects. Each object should have 'Type' (Active/Passive), 'Timer' (integer in seconds), and 'Description' (text)."
    )
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title  # Fixed incorrect capitalization

    def formatted_directions(self):
        """Return formatted directions for display."""
        return "\n".join([
            f"{step['Type']} - {step['Timer']}s: {step['Description']}" 
            for step in self.directions
        ])
