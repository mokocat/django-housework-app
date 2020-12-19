import datetime

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class RecipeCategory(models.Model):
    category_name = models.CharField(max_length=20)  # 例）中華、和食、イタリアン
    priority = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.category_name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=20)  # 例）ジャガイモ、ニンジン、牛肉
    ingredient_name_romaji = models.CharField(max_length=20)  # 例）Jagaimo,Ninjin,Gyuniku
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.ingredient_name


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=50)  # 例）カレー
    recipe_name_romaji = models.CharField(max_length=50)  # 例）Kare
    recipe_file = models.FileField(
        blank=True,
        null=True,
    )
    recipe_url = models.URLField(blank=True, max_length=2000)  # クックパッド等のURL
    categories = models.ManyToManyField(RecipeCategory, blank=True)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    remark = models.CharField(max_length=50, blank=True)  # 備考　例）塩は少なめ
    review = models.IntegerField(blank=True, null=True, default=3)  # 例）５
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.recipe_name


class MealPlan(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)
    meal_plan_name = models.CharField(max_length=50)
    meal_plan_date = models.DateField()
    categories = models.ManyToManyField(RecipeCategory, blank=True)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.meal_plan_name


class Shop(models.Model):
    shop_name = models.CharField(max_length=20)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.shop_name


class ShoppingItemPicture(models.Model):
    shopping_item_picture_name = models.CharField(max_length=20)
    shopping_item_picture_name_romaji = models.CharField(max_length=20)
    picture = models.FileField()
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.shopping_item_picture_name

@receiver(post_delete, sender=ShoppingItemPicture)
def delete_file(sender, instance, **kwargs):
    instance.picture.delete(False)

class ShoppingItem(models.Model):
    item = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    shopping_item_date = models.DateField(default=datetime.date.today)
    shop = models.ForeignKey(Shop, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    shopping_item_picture = models.ForeignKey(ShoppingItemPicture, null=True, blank=True, default=None,
                                              on_delete=models.SET_NULL)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.item
