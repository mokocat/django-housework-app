import datetime

from dateutil import relativedelta
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from pykakasi import kakasi

kakasi = kakasi()
kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

log = logging.getLogger(__name__)

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):    
    # to cover more complex cases:
    # http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    ip = request.META.get('REMOTE_ADDR')

    log.info('login user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs): 
    ip = request.META.get('REMOTE_ADDR')

    log.info('logout user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    log.warning('login failed for: {credentials}'.format(
        credentials=credentials,
    ))

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Top(LoginRequiredMixin, generic.TemplateView):
    template_name = 'top.html'


def romaji_convert(name):
    conv = kakasi.getConverter()
    return conv.do(name)


def delete_something_element(request, model, element_id, redirect_name):
    item = model.objects.get(pk=element_id)
    item.delete()
    messages.success(request, ('Deleted successfully!'))
    return redirect(redirect_name)


def change_status_of_shopping_item(request, model, status, element_id, redirect_name):
    item = model.objects.get(pk=element_id)
    item.completed = status
    item.save()
    return redirect(redirect_name)


def show_items_for_1_year(model, request, range_name, redirect_name):
    today = datetime.date.today()
    end_time = today + relativedelta.relativedelta(years=1)
    args = []
    kwargs = {"user": request.user, range_name: (today, end_time)}
    return model.objects.filter(*args, **kwargs).order_by(redirect_name)


def create_item(request, form_name):
    if request.method == 'POST':
        form = form_name(request.POST or None)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, ('Created successfully!'))
        else:
            messages.success(request, ('error!'))


def get_old_date_items(request, model, range_name, **additional_condition):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    args = []
    kwargs = {"user": request.user, range_name: ("2020-1-1", yesterday)}
    kwargs_2 = additional_condition
    kwargs.update(kwargs_2)
    return model.objects.filter(*args, **kwargs)


def form_valid_and_romaji_convert(request, form, name_field, name_romaji_field):
    if form.is_valid():
        question = form.save(commit=False)
        r = getattr(question, name_field)
        setattr(question, name_romaji_field, romaji_convert(r))
        question.save()
        messages.success(request, ('regisitered successfully!'))
    else:
        messages.success(request, ('error!'))


def form_view_valid_and_romaji_convert(form, self, user_register, name_field, name_romaji_field):
    if user_register:
        form.instance.user_id = self.request.user.id
    question = form.save(commit=False)
    r = getattr(question, name_field)
    setattr(question, name_romaji_field, romaji_convert(r))
    question.save()
