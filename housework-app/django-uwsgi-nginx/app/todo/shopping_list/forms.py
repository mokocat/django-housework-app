from django import forms

from todo.models import Shop, ShoppingItemPicture


class CreateShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ["shop_name"]


class CreateShoppingItemPictureForm(forms.ModelForm):
    class Meta:
        model = ShoppingItemPicture
        fields = ['shopping_item_picture_name', 'picture']
