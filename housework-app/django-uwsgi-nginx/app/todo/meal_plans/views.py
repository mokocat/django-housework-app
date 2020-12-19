from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from todo.common import mixins
from todo.common.views import delete_something_element
from todo.meal_plans.forms import CreateMealPlanForm, CreateMealPlanFromRecipeForm, UpdateMealPlanForm
from todo.models import MealPlan, Recipe


class ShowAndCreateMealPlanView(mixins.WeekWithScheduleMixin, generic.CreateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'meal_plans/show_and_create_meal_plan.html'
    model = MealPlan
    date_field = 'meal_plan_date'
    form_class = CreateMealPlanForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context

    def get_form_kwargs(self):
        kwargs = super(ShowAndCreateMealPlanView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.save()
        return redirect('show_and_create_meal_plan')


class CreateMealPlanFromRecipeFormView(BSModalCreateView):
    template_name = 'create_modal_form.html'
    form_class = CreateMealPlanFromRecipeForm
    success_message = 'Success: MealPlan was created.'
    success_url = reverse_lazy('show_and_create_meal_plan')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        id = self.kwargs['pk']
        date = form.data['meal_plan_date']
        obj = form.save(commit=False)
        obj.recipe = Recipe.objects.get(pk=id)
        obj.meal_plan_name = obj.recipe.recipe_name
        obj.meal_plan_date = date
        obj.save()
        category = obj.recipe.categories.all()
        for i in category:
            obj.categories.add(i)
        return super(CreateMealPlanFromRecipeFormView, self).form_valid(form)


class UpdateMealPlanFormView(BSModalUpdateView):
    model = MealPlan
    template_name = 'update_meal_plan_modal_form.html'
    form_class = UpdateMealPlanForm
    success_url = reverse_lazy('show_and_create_meal_plan')

    def get_form_kwargs(self):
        kwargs = super(UpdateMealPlanFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def delete_meal_plan(request, meal_plan_id):
    return delete_something_element(request, MealPlan, meal_plan_id, 'show_and_create_meal_plan')
