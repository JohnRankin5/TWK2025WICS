from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.JSONField(
        default=list,
        help_text="List of ingredients as a JSON array (e.g., ['2 eggs', '1 cup sugar'])."
    )
    directions = models.JSONField(
        default=list,
        help_text="List of steps, each containing 'Active' and 'Passive' keys."
    )
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
