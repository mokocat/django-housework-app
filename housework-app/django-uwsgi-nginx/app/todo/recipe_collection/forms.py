from bootstrap_modal_forms.forms import BSModalForm
from django import forms

from todo.models import Recipe, RecipeCategory, Ingredient


class CreateUpdateRecipeForm(BSModalForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'recipe_file', 'recipe_url', 'categories', 'ingredients', 'remark', 'review']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreateUpdateRecipeForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = RecipeCategory.objects.filter(user=user)
        self.fields['ingredients'].queryset = Ingredient.objects.filter(user=user)


class CreateRecipeCategoryForm(forms.ModelForm):
    class Meta:
        model = RecipeCategory
        fields = ["category_name"]


class CreateIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["ingredient_name"]


class UpdateRecipeCategoryForm(BSModalForm):
    class Meta:
        model = RecipeCategory
        fields = ['category_name', 'priority']
