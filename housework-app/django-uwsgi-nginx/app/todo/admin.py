from django.contrib import admin

# Register your models here.
from todo.models import ShoppingItem, Shop, ShoppingItemPicture, MealPlan, Recipe, Ingredient, RecipeCategory

admin.site.register(ShoppingItem)
admin.site.register(Shop)
admin.site.register(ShoppingItemPicture)
admin.site.register(MealPlan)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeCategory)
