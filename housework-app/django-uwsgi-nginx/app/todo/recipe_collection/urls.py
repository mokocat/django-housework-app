from django.urls import path
from todo.recipe_collection import views

urlpatterns = [
    path('recipe_collection/', views.show_recipe, name='show_recipe'),
    path('create_recipe/', views.CreateRecipeFormView.as_view(), name='create_recipe'),
    path('search_recipe_by_recipe_name/', views.search_recipe_by_recipe_name, name='search_recipe_by_recipe_name'),
    path('search_recipe_by_ingredient/', views.search_recipe_by_ingredient, name='search_recipe_by_ingredient'),
    path('search_recipe_by_category/', views.search_recipe_by_category, name='search_recipe_by_category'),
    path('update_recipe/<int:pk>', views.UpdateRecipeFormView.as_view(), name='update_recipe'),
    path('delete_recipe/<recipe_id>', views.delete_recipe, name='delete_recipe'),
    path('show_recipe_category_and_ingredient/', views.show_recipe_category_and_ingredient,
         name='show_recipe_category_and_ingredient'),
    path('create_recipe_category/', views.create_recipe_category, name='create_recipe_category'),
    path('create_recipe_ingredient/', views.create_recipe_ingredient, name='create_recipe_ingredient'),
    path('update_recipe_category/<int:pk>', views.UpdateRecipeCategoryFormView.as_view(),
         name='update_recipe_category'),
    path('delete_category/<category_id>', views.delete_category, name='delete_category'),
    path('delete_ingredient/<ingredient_id>', views.delete_ingredient, name='delete_ingredient'),
]
