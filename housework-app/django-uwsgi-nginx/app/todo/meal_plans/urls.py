from django.urls import path
from todo.meal_plans import views

urlpatterns = [
    path('create_meal_plan_from_recipe/<int:pk>', views.CreateMealPlanFromRecipeFormView.as_view(),
         name='create_meal_plan_from_recipe'),
    path('update_meal_plan/<int:pk>', views.UpdateMealPlanFormView.as_view(), name='update_meal_plan'),
    path('delete_meal_plan/<meal_plan_id>', views.delete_meal_plan, name='delete_meal_plan'),
    path('meal_plan/', views.ShowAndCreateMealPlanView.as_view(), name='show_and_create_meal_plan'),
    path('meal_plan/<int:year>/<int:month>/<int:day>/', views.ShowAndCreateMealPlanView.as_view(),
         name='show_and_create_meal_plan')
]
