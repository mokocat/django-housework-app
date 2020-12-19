from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from todo.models import MealPlan, Recipe, RecipeCategory


class CreateMealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['meal_plan_name', 'meal_plan_date', 'categories']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreateMealPlanForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = RecipeCategory.objects.filter(user=user).order_by('priority')


class CreateMealPlanFromRecipeForm(BSModalForm):
    class Meta:
        model = MealPlan
        fields = ['meal_plan_date']


class UpdateMealPlanForm(BSModalForm):
    class Meta:
        model = MealPlan
        fields = ['meal_plan_name', 'meal_plan_date', 'recipe', 'categories']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateMealPlanForm, self).__init__(*args, **kwargs)
        self.fields['recipe'].queryset = Recipe.objects.filter(user=user)
        self.fields['categories'].queryset = RecipeCategory.objects.filter(user=user).order_by('priority')
