import datetime
import json

from bulk_update.helper import bulk_update
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render
from django.views import generic
from todo.common.views import delete_something_element, create_item, \
    get_old_date_items, form_valid_and_romaji_convert
from todo.models import ShoppingItem, ShoppingItemPicture, Shop
from todo.shopping_list.forms import CreateShoppingItemPictureForm, CreateShopForm

def show_shop_and_shopping_item_picture_setting(request):
    shops = Shop.objects.filter(user=request.user)
    picture = ShoppingItemPicture.objects.filter(user=request.user)
    return render(request, 'shopping_list/show_shop_and_shopping_item_picture_setting.html',
                  {'shops': shops, 'picture': picture})


def create_shop(request):
    create_item(request, CreateShopForm)
    return show_shop_and_shopping_item_picture_setting(request)


def create_shopping_item_picture(request):
    if request.method == 'POST':
        form = CreateShoppingItemPictureForm(request.POST, request.FILES)
        form.instance.user = request.user
        form_valid_and_romaji_convert(request, form, "shopping_item_picture_name", "shopping_item_picture_name_romaji")
    return show_shop_and_shopping_item_picture_setting(request)


def delete_shop(request, shop_id):
    return delete_something_element(request, Shop, shop_id, 'show_shop_and_shopping_item_picture_setting')


def delete_shopping_item_picture(request, pic_id):
    return delete_something_element(request, ShoppingItemPicture, pic_id, 'show_shop_and_shopping_item_picture_setting')


class ShowShoppingItemView(generic.TemplateView):
    template_name = "shopping_list/show_shopping_item.html"


def get_shopping_item(request):
    # delete old date completed item
    old_items = get_old_date_items(request, ShoppingItem, 'shopping_item_date__range', completed=True)
    old_items.delete()

    # update old date uncompleted item to today
    not_completed_items = get_old_date_items(request, ShoppingItem, 'shopping_item_date__range', completed=False)
    today = datetime.date.today()
    for item in not_completed_items:
        item.shopping_item_date = today
    bulk_update(not_completed_items, update_fields=['shopping_item_date'])

    items = ShoppingItem.objects.filter(user=request.user).order_by("completed", "shopping_item_date", "shop").values()
    item_list = list(items)
    shops = Shop.objects.filter(user=request.user).values()
    shop_list = list(shops)
    pictures = ShoppingItemPicture.objects.filter(user=request.user).values()
    picture_list = list(pictures)
    all_lists = {"all_items": item_list, "shops": shop_list, "pictures": picture_list}
    return JsonResponse(all_lists, safe=False)


def post_update_shopping_item(request):
    if request.method == 'POST' and request.body:
        json_dict = json.loads(request.body)
        item = json_dict['item']
        shopping_item_date = json_dict['shopping_item_date']
        user = request.user
        completed = json_dict['completed']
        if not ('item_id' in json_dict.keys()):
            ShoppingItem.objects.create(item=item, shopping_item_date=shopping_item_date, completed=completed,
                                        user=user)
        else:
            item_id = json_dict['item_id']
            all_items = ShoppingItem.objects.get(pk=item_id)
            shop_id = json_dict['shop_id']
            picture_id = json_dict['picture_id']
            all_items.item = item
            all_items.shopping_item_date = shopping_item_date
            all_items.completed = completed
            all_items.shopping_item_picture_id = picture_id
            all_items.shop_id = shop_id
            all_items.save()
        return get_shopping_item(request)
    else:
        return HttpResponseServerError()


def post_delete_shopping_item(request):
    if request.method == 'POST' and request.body:
        json_dict = json.loads(request.body)
        item_id = json_dict['item_id']
        item = ShoppingItem.objects.get(pk=item_id)
        item.delete()
        return get_shopping_item(request)
    else:
        return HttpResponseServerError()
