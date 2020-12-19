import datetime
import errno
import json
import os
import socket
import time

from bs4 import BeautifulSoup
from config.settings.base import BASE_DIR
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.servers.basehttp import ThreadedWSGIServer
from django.test import RequestFactory, TestCase
from django.test.testcases import QuietWSGIRequestHandler, LiveServerThread
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from todo.meal_plans import views as meal_plan_view
from todo.models import Shop, ShoppingItemPicture, Recipe, MealPlan, RecipeCategory, Ingredient
from todo.recipe_collection import views as recipe_view
from todo.shopping_list import views as shopping_list_view


class TestShoppingItemList(TestCase):
    fixtures = ['testdb.json']

    def __init__(self, *args, **kwargs):
        super(TestShoppingItemList, self).__init__(*args, **kwargs)
        self.user = None
        self.rf = None

    @classmethod
    def getbs(cls, res):
        return BeautifulSoup(res.content, 'html.parser')

    @classmethod
    def initialize_req(cls, req):
        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)

    def setUp(self):
        self.user = User.objects.get(username="guest1")
        self.rf = RequestFactory()

    def test_get_shopping_item(self):
        req = self.rf.get("/app/shopping_list/get_shopping_item/")
        req.user = self.user
        res = shopping_list_view.get_shopping_item(req)
        self.assertEqual(res.status_code, 200)
        content = json.loads(res.content)
        item = content['all_items']
        self.assertEqual("Item1", item[0]['item'])

    def test_create_shop(self):
        shop_name = "Shop3"
        req = self.rf.post("/app/shopping_list/shop_and_shopping_item_picture_setting/",
                           data={"shop_name": shop_name})
        req.user = self.user
        self.initialize_req(req)
        res = shopping_list_view.create_shop(req)
        self.assertEqual(res.status_code, 200)
        bs = self.getbs(res)
        self.assertEqual(shop_name, bs.find(id="3-shop").text)
        self.assertEqual(None, bs.find(id="1-shop"))

    def test_delete_shop(self):
        req = self.rf.post("/app/shopping_list/delete_shop/2")
        req.user = self.user
        self.initialize_req(req)
        res = shopping_list_view.delete_shop(req, 2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Shop.objects.count(), 1)

    def test_create_shopping_item_picture(self):
        item = "Picture3"
        png_file = "todo/fixtures/pic.png"
        upload_pic = 'media/pic.png'
        with open(png_file, 'rb') as f:
            req = self.rf.post("/app/shopping_list/shop_and_shopping_item_picture_setting/",
                               data={"shopping_item_picture_name": item, "picture": f},
                               format='multipart')
        req.user = self.user
        self.initialize_req(req)
        res = shopping_list_view.create_shopping_item_picture(req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(ShoppingItemPicture.objects.get(pk=3).shopping_item_picture_name, item)
        os.remove(upload_pic)

    def test_delete_shopping_item_picture(self):
        png_file = "todo/fixtures/pic.png"
        req = self.rf.post("/app/shopping_list/delete_shopping_item_picture/2")
        req.user = self.user
        self.initialize_req(req)
        res = shopping_list_view.delete_shopping_item_picture(req, 2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(ShoppingItemPicture.objects.count(), 1)

    def test_create_recipe(self):
        recipe_name = "Recipe3"
        req = self.rf.post("/app/recipe_collection/create_recipe/",
                           data={"recipe_name": recipe_name, "review": 3, "categories": 2, "ingredients": 2})
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.CreateRecipeFormView.as_view()(req)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Recipe.objects.get(pk=3).recipe_name, recipe_name)

    def test_update_recipe(self):
        recipe_name = "Recipe3"
        req = self.rf.post("/app/recipe_collection/update_recipe/2",
                           data={"recipe_name": recipe_name})
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.UpdateRecipeFormView.as_view()(req, pk=2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Recipe.objects.get(pk=2).recipe_name, recipe_name)

    def test_delete_recipe(self):
        req = self.rf.post("/app/recipe_collection/delete_recipe/2")
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.delete_recipe(req, 2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_search_recipe_by_recipe_name(self):
        recipe_name = "recipe"
        req = self.rf.get("/app/recipe_collection/search_recipe_by_recipe_name/", data={"name": recipe_name})
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.search_recipe_by_recipe_name(req)
        self.assertEqual(res.status_code, 200)
        bs = self.getbs(res)
        self.assertEqual("Recipe1", bs.find(id="2-recipe_name").text.strip())

    def test_search_recipe_by_ingredient(self):
        ingredient_name = "ingredient"
        req = self.rf.get("/app/recipe_collection/search_recipe_by_ingredient/", data={"name": ingredient_name})
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.search_recipe_by_ingredient(req)
        self.assertEqual(res.status_code, 200)
        bs = self.getbs(res)
        self.assertEqual("Recipe1", bs.find(id="2-recipe_name").text.strip())

    def search_recipe_by_category(self):
        category = "Category1"
        req = self.rf.get("/app/recipe_collection/search_recipe_by_category/", data={"name": category})
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.search_recipe_by_category(req)
        self.assertEqual(res.status_code, 200)
        bs = self.getbs(res)
        self.assertEqual("Recipe1", bs.find(id="2-recipe_name").text.strip())

    def test_create_meal_plan_from_recipe(self):
        date = "2020-06-04"
        req = self.rf.post("/app/recipe_collection/create_meal_plan_from_recipe/",
                           data={"meal_plan_date": date})
        req.user = self.user
        self.initialize_req(req)
        res = meal_plan_view.CreateMealPlanFromRecipeFormView.as_view()(req, pk=2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(MealPlan.objects.get(pk=3).meal_plan_name, "Recipe1")

    def test_create_category(self):
        category_name = "Category3"
        req = self.rf.post("/app/recipe_collection/create_recipe_category/",
                           data={"category_name": category_name})
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.create_recipe_category(req)
        self.assertEqual(res.status_code, 200)
        bs = self.getbs(res)
        self.assertEqual(category_name, bs.find(id="3-category_name").text)
        self.assertEqual(None, bs.find(id="1-category_name"))

    def test_update_category(self):
        category_name = "Category3"
        req = self.rf.post("/app/recipe_collection/update_recipe_category/2",
                           data={"category_name": category_name})
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.UpdateRecipeCategoryFormView.as_view()(req, pk=2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(RecipeCategory.objects.get(pk=2).category_name, category_name)

    def test_delete_category(self):
        req = self.rf.post("/app/recipe_collection/delete_category/2")
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.delete_category(req, 2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(RecipeCategory.objects.count(), 1)

    def test_create_recipe_ingredient(self):
        ingredient_name = "Ingredient3"
        req = self.rf.post("/app/recipe_collection/create_recipe_ingredient/",
                           data={"ingredient_name": ingredient_name})
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.create_recipe_ingredient(req)
        self.assertEqual(res.status_code, 200)
        bs = self.getbs(res)
        self.assertEqual(ingredient_name, bs.find(id="3-ingredient_name").text)
        self.assertEqual(None, bs.find(id="1-ingredient_name"))

    def test_delete_ingredient(self):
        req = self.rf.post("/app/recipe_collection/delete_ingredient/2")
        req.user = self.user
        self.initialize_req(req)
        res = recipe_view.delete_ingredient(req, 2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_create_meal_plan(self):
        meal_plan_name = "Meal3"
        req = self.rf.post("/app/meal_plans/meal_plan/",
                           data={"meal_plan_name": meal_plan_name, "meal_plan_date": '2020-06-05', "categories": 2})
        req.user = self.user
        self.initialize_req(req)
        res = meal_plan_view.ShowAndCreateMealPlanView.as_view()(req)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(MealPlan.objects.get(pk=3).meal_plan_name, meal_plan_name)

    def test_update_meal_plan(self):
        meal_plan_name = "Meal3"
        req = self.rf.post("/app/meal_plans/update_meal_plan/2",
                           data={"meal_plan_name": meal_plan_name, "meal_plan_date": "2020-06-10", "categories": 2})
        req.user = self.user
        self.initialize_req(req)
        res = meal_plan_view.UpdateMealPlanFormView.as_view()(req, pk=2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(MealPlan.objects.get(pk=2).meal_plan_name, meal_plan_name)

    def test_delete_meal_plan(self):
        req = self.rf.post("/app/meal_plans/delete_meal_plan/2")
        req.user = self.user
        self.initialize_req(req)
        res = meal_plan_view.delete_meal_plan(req, 2)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(MealPlan.objects.count(), 1)


class ConnectionResetErrorSwallowingQuietWSGIRequestHandler(QuietWSGIRequestHandler):
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except socket.error as err:
            if err.errno != errno.WSAECONNRESET:
                raise


class ConnectionResetErrorSwallowingLiveServerThread(LiveServerThread):
    def _create_server(self):
        return ThreadedWSGIServer((self.host, self.port), ConnectionResetErrorSwallowingQuietWSGIRequestHandler,
                                  allow_reuse_address=False)


class AdminSiteTestCase(StaticLiveServerTestCase):
    server_thread_class = ConnectionResetErrorSwallowingLiveServerThread


class SmokeTest(AdminSiteTestCase):
    fixtures = ['testdb.json']
    timeout = 30
    trial = 10

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        chrome_driver = "chromedriver.exe" if os.name == "nt" else "chromedriver"
        cls.driver = WebDriver(options=options, executable_path=f'{os.getcwd()}/static/test/{chrome_driver}')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def wait_model_open(self, driver):
        for i in range(self.trial):
            class_att = driver.find_element_by_tag_name("body").get_attribute("class")
            if class_att == "modal-open":
                return
            time.sleep(1)
        raise Exception("time out!")

    def wait_for_element_exist(self, driver, eid):
        WebDriverWait(driver, self.timeout).until(EC.element_to_be_clickable((By.ID, eid)))

    def wait_for_element_not_exist(self, driver, eid):
        WebDriverWait(driver, self.timeout).until(EC.invisibility_of_element((By.ID, eid)))

    def test_gui(self):
        timeout = 30
        d = SmokeTest.driver

        # Login app site
        d.get(self.live_server_url + '/app/')
        self.assertEquals("Login", d.title)
        d.find_element_by_id("id_username").send_keys("guest1")
        d.find_element_by_id("id_password").send_keys("guest1guest1")
        d.find_element_by_class_name("submit").click()

        # Access to shopping list page
        self.assertEquals("Top Page", d.title)
        d.find_element_by_class_name("navbar-toggler").click()
        self.wait_for_element_exist(d, "shopping_list_page")
        d.find_element_by_id("shopping_list_page").click()

        # Check shopping item
        self.assertEquals("買物リスト", d.title)
        self.wait_for_element_exist(d, "2-item")
        item = d.find_element_by_id("2-item").text
        self.assertEquals(item, "Item1")

        # Create shop
        d.find_element_by_class_name("navbar-toggler").click()
        self.wait_for_element_exist(d, "shop_and_picture_setting_page")
        d.find_element_by_id("shop_and_picture_setting_page").click()
        shop_name = "Shop3"
        shop = d.find_element_by_id("shop_name")
        shop.clear()
        shop.send_keys(shop_name)
        d.find_element_by_id("shop_save_btn").click()
        new_shop = d.find_element_by_id("3-shop").text
        self.assertEquals(new_shop, shop_name)

        # Create picture
        picture_name = "Picture3"
        picture = d.find_element_by_id("picture_name")
        picture.clear()
        picture.send_keys(picture_name)
        picture_file = d.find_element_by_id("inputFile")
        picture_file.clear()
        url = BASE_DIR + "/todo/fixtures/pic.png"
        upload_pic = BASE_DIR + '/media/pic.png'
        picture_file.send_keys(url)
        d.find_element_by_id("picture_save_btn").click()
        new_shop = d.find_element_by_id("3-picture_name").text
        self.assertEquals(new_shop, picture_name)
        os.remove(upload_pic)

        # Create shopping item
        d.find_element_by_class_name("navbar-toggler").click()
        self.wait_for_element_exist(d, "shopping_list_page")
        d.find_element_by_id("shopping_list_page").click()
        item_name = "Item3"
        item_form = d.find_element_by_id("item")
        item_form.clear()
        item_form.send_keys(item_name)
        d.find_element_by_id("item_save_btn").click()
        self.wait_for_element_exist(d, "3-item")
        new_item = d.find_element_by_id("3-item").text
        self.assertEquals(new_item, item_name)

        # Update shopping item
        d.find_element_by_id("3-edit").click()
        item_shop = d.find_element_by_name("select_shop")
        item_shop_select = Select(item_shop)
        item_shop_select.select_by_value(shop_name)
        item_picture = d.find_element_by_name("select_picture")
        item_picture_select = Select(item_picture)
        item_picture_select.select_by_visible_text(picture_name)
        self.wait_for_element_exist(d, "3-edit")
        d.find_element_by_id("3-edit").click()
        self.wait_for_element_exist(d, "3-item")
        self.assertEquals(d.find_element_by_id("3-item").text, item_name)
        self.assertEquals(d.find_element_by_id("3-shop").text, shop_name)

        # Create category
        d.find_element_by_class_name("navbar-toggler").click()
        self.wait_for_element_exist(d, "category_and_ingredient_setting_page")
        d.find_element_by_id("category_and_ingredient_setting_page").click()
        category_name = "Category3"
        category = d.find_element_by_id("category_name")
        category.clear()
        category.send_keys(category_name)
        d.find_element_by_id("category_save_btn").click()
        new_category = d.find_element_by_id("3-category_name").text
        self.assertEquals(new_category, category_name)

        # Create ingredient
        ingredient_name = "Ingredient3"
        ingredient = d.find_element_by_id("ingredient_name")
        ingredient.clear()
        ingredient.send_keys(ingredient_name)
        d.find_element_by_id("ingredient_save_btn").click()
        new_ingredient = d.find_element_by_id("3-ingredient_name").text
        self.assertEquals(new_ingredient, ingredient_name)

        # Create Recipe
        d.find_element_by_class_name("navbar-toggler").click()
        self.wait_for_element_exist(d, "recipe_collection_page")
        d.find_element_by_id("recipe_collection_page").click()
        d.find_element_by_id("recipe_create_btn").click()
        recipe_name = "Recipe3"
        self.wait_for_element_exist(d, "id_recipe_name")
        recipe = d.find_element_by_id("id_recipe_name")
        recipe.clear()
        recipe.send_keys(recipe_name)
        url_path = "https://www.google.co.jp/"
        url = d.find_element_by_id("id_recipe_url")
        url.clear()
        url.send_keys(url_path)
        self.wait_for_element_exist(d, "id_categories")
        categories = d.find_element_by_id("id_categories")
        categories_select = Select(categories)
        categories_select.select_by_value("3")
        ingredients = d.find_element_by_id("id_ingredients")
        ingredients_select = Select(ingredients)
        ingredients_select.select_by_value("3")
        d.find_element_by_id("create").click()
        self.wait_for_element_exist(d, "3-recipe_name")
        self.assertEquals(d.find_element_by_id("3-recipe_name").text, recipe_name)
        create_recipe_url = d.find_element_by_id("3-recipe_name").find_element_by_tag_name("a")
        self.assertEquals(create_recipe_url.get_attribute("href"), url_path)

        # Search Recipe
        ingredient_search = d.find_element_by_id("ingredient_name").find_element_by_tag_name("input")
        ingredient_search.clear()
        ingredient_search.send_keys(ingredient_name)
        d.find_element_by_id("ingredient_name_btn").click()
        self.assertEquals(d.find_element_by_id("3-recipe_name").text, recipe_name)
        self.assertEquals([], d.find_elements_by_id("2-recipe_name"))

        # Create meal plan
        d.find_element_by_id("3-register_meal_plan").click()
        self.wait_for_element_exist(d, "id_meal_plan_date")
        meal_plan_date = d.find_element_by_id("id_meal_plan_date")
        meal_plan_date.clear()
        today_obj = datetime.date.today()
        today = str(today_obj)
        input_date = '00' + today_obj.strftime('%Y%m%d')
        meal_plan_date.send_keys(input_date)
        d.find_element_by_id("create").click()
        meal_plan_id = today + '_' + category_name
        create_meal_plan = d.find_element_by_id(meal_plan_id)
        self.assertEquals(create_meal_plan.text, recipe_name)
        create_meal_plan_url = create_meal_plan.find_element_by_tag_name("a")
        self.assertEquals(create_meal_plan_url.get_attribute("href"), url_path)

        # Update meal plan
        create_meal_plan.find_element_by_tag_name("img").click()
        self.wait_for_element_exist(d, "id_categories")
        categories = d.find_element_by_id("id_categories")
        categories_select = Select(categories)
        categories_select.select_by_value("2")
        d.find_element_by_id("update").click()
        meal_plan_id = today + '_Category1'
        update_recipe = d.find_element_by_id(meal_plan_id)
        self.assertEquals(update_recipe.text, recipe_name)
