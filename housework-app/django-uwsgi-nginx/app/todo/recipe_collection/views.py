from bootstrap_modal_forms.generic import BSModalUpdateView, BSModalCreateView
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy

from todo.common.views import romaji_convert, delete_something_element, create_item, form_valid_and_romaji_convert, \
    form_view_valid_and_romaji_convert
from todo.models import Recipe, RecipeCategory, Ingredient
from todo.recipe_collection.forms import CreateUpdateRecipeForm, CreateRecipeCategoryForm, CreateIngredientForm, \
    UpdateRecipeCategoryForm


def show_recipe(request):
    all_items = Recipe.objects.filter(user=request.user)
    return show_select_category(request, all_items)


def show_select_category(request, all_items):
    categories = RecipeCategory.objects.filter(user=request.user)
    return render(request, 'recipe_collection/show_recipe.html', {'all_items': all_items, 'form': categories})


class CreateRecipeFormView(BSModalCreateView):
    template_name = 'create_modal_form.html'
    form_class = CreateUpdateRecipeForm
    success_message = 'Success: Recipe was created.'
    success_url = reverse_lazy('show_recipe')

    def get_form_kwargs(self):
        kwargs = super(CreateRecipeFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form_view_valid_and_romaji_convert(form, self, True, "recipe_name", "recipe_name_romaji")
        return super(CreateRecipeFormView, self).form_valid(form)


class UpdateRecipeFormView(BSModalUpdateView):
    model = Recipe
    template_name = 'update_modal_form.html'
    form_class = CreateUpdateRecipeForm
    success_message = 'Success: Recipe was updated.'
    success_url = reverse_lazy('show_recipe')

    def get_form_kwargs(self):
        kwargs = super(UpdateRecipeFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form_view_valid_and_romaji_convert(form, self, False, "recipe_name", "recipe_name_romaji")
        return super(UpdateRecipeFormView, self).form_valid(form)


def search_recipe_by_recipe_name(request):
    name = request.GET.get('name')
    romaji_name = romaji_convert(request.GET.get('name'))
    all_items = Recipe.objects.filter(Q(recipe_name_romaji__icontains=romaji_name) |
                                      Q(recipe_name__icontains=name), Q(user=request.user))
    return show_select_category(request, all_items)


def search_recipe_by_ingredient(request):
    name = request.GET.get('name')
    romaji_name = romaji_convert(request.GET.get('name'))
    all_items = Recipe.objects.filter(Q(ingredients__ingredient_name_romaji__icontains=romaji_name) |
                                      Q(ingredients__ingredient_name__icontains=name), Q(user=request.user))
    return show_select_category(request, all_items)


def search_recipe_by_category(request):
    name = request.GET.get('name')
    all_items = Recipe.objects.filter(user=request.user, categories__category_name=name)
    return show_select_category(request, all_items)


def delete_recipe(request, recipe_id):
    return delete_something_element(request, Recipe, recipe_id, 'show_recipe')


def show_recipe_category_and_ingredient(request):
    categories = RecipeCategory.objects.filter(user=request.user).order_by('priority')
    ingredients = Ingredient.objects.filter(user=request.user)
    return render(request, 'recipe_collection/recipe_category_and_ingredient_setting.html',
                  {'categories': categories, 'ingredients': ingredients})


def create_recipe_category(request):
    create_item(request, CreateRecipeCategoryForm)
    return show_recipe_category_and_ingredient(request)


def create_recipe_ingredient(request):
    if request.method == 'POST':
        form = CreateIngredientForm(request.POST or None)
        form.instance.user = request.user
        form_valid_and_romaji_convert(request, form, "ingredient_name", "ingredient_name_romaji")
    return show_recipe_category_and_ingredient(request)


class UpdateRecipeCategoryFormView(BSModalUpdateView):
    model = RecipeCategory
    template_name = 'update_modal_form.html'
    form_class = UpdateRecipeCategoryForm
    success_message = 'Success: Category was updated.'
    success_url = reverse_lazy('show_recipe_category_and_ingredient')


def delete_category(request, category_id):
    return delete_something_element(request, RecipeCategory, category_id, 'show_recipe_category_and_ingredient')


def delete_ingredient(request, ingredient_id):
    return delete_something_element(request, Ingredient, ingredient_id, 'show_recipe_category_and_ingredient')
