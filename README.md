# Housework-management-app
 
- This is a web application for management your housework !
- This app is simple CRUD app (partially used Ajax) packaged with django-uwsgi-nginx-https docker image.
- You can soon run and develop your own web app based on this package.
 
# DEMO
 
## please access to the following demo app page !
- https://housework.mokocat.com/app/
* This page is subject to be inaccessible or change without notice.

## Usage
1. Access to [signup page](https://housework.mokocat.com/app/signup/).
1. Access to [login page](https://housework.mokocat.com/accounts/login/) and input your username and password.
1. Register [recipe category](https://housework.mokocat.com/app/recipe_collection/show_recipe_category_and_ingredient/). (meal plan was shown by this category orderd by the registered priority.)

# Features
 
## This app has 3 features.
### 1. Shopping list
![shopping_list](https://user-images.githubusercontent.com/59159469/94521566-3e00e600-0269-11eb-9e68-95574d5f5c93.png)
- You can register your shopping item, date, shop and photo.
- You can check the bought shopping items.
- If you can't buy item today, the item will automatically transfer the following day.
### 2. Recipe collection
![recipe_collection](https://user-images.githubusercontent.com/59159469/94521647-612b9580-0269-11eb-823a-1e235c310385.png)
- You can register your recipe url or file.
- You can search recipe by name, ingredient or category.
### 3. Meal plan
![meal_plan](https://user-images.githubusercontent.com/59159469/94521687-70124800-0269-11eb-9eec-2ea763f737ed.png)
- You can register your meal plan by manual input.
- You can register meal plan from recipe collection.
- The meal plan was shown by your category.

## This app specification is in the following directory.
- django-housework-app\housework-app\django-uwsgi-nginx\app\doc
    - housework-app_requiremnets.md: requirements definition
    - housework-app_usecase.puml: use case diagram
    - housework-app_screen.md: screen list

# Installation
## When you use Docker container (when you want to run this app soon.)
### The app runs with uWSGI and use settings/production.py
1. Clone or download zip of this project.
1. Open 'django-housework-app'(project) folder.
1. Create the .env file under the following directory.
    - django-housework-app\housework-app\django-uwsgi-nginx\app
1. Open the .env file and write the following code
    ```bash
    SECRET_KEY=t@vl8u$$uirv_omcs*uo6o%3%1^!t_8*1l*%n=me6r+ox-l5+6
    DEBUG=False
    ALLOWED_HOSTS=housework-app-local.com
    ```
    *when you run app in production mode, you should change the SECRET_KEY.
1. If you use other domain, change the DOMAINS in the following file. *default domain is 'housework-app-local.com'.
    - django-housework-app\housework-app\docker-compose.yml
1. Add the following in C:\Windows\System32\drivers\etc\hosts (Windows).　 *please save as administrator. *You should use the [Half-width space] or [Tab] key between the IP address and the host name.
    - 127.0.0.1   housework-app-local.com
1. Move to housework-app directory.
    ```bash
    cd housework-app
    ```
1. Run docker-compose file.
    ```bash
    docker-compose up
    ```
1. After building, access to the following url.
    - https://housework-app-local.com/app
1. Click ADVANCED, then click Proceed to housework-app-local.com (unsafe).
1. If you want to run app in production mode, please change the following code in housework-app\docker-compose.yml.
* Detail explanation is written in [SteveLTN/https-portal page](https://github.com/SteveLTN/https-portal). 
    - 'DOMAINS': change from housework-app-local.com to 'your domain'.
    - 'STAGE': change from 'local' to 'staging' or 'production'.

    ```bash
    environment:
      # please change to your domain.
      DOMAINS: 'housework-app-local.com -> http://django:50000'
      STAGE: 'local'
      CLIENT_MAX_BODY_SIZE: 10M
    ```
 

## When you use local environment without docker (when you want to develop or test using this app)
### The app runs with manage.py runserver and use settings/local.py
* This procedure is using Visual Studio Code.
1. Install Visual studio code.
    - https://code.visualstudio.com/download
1. Clone or download zip of this project to your local.
1. Open 'app' folder
    - django-housework-app\housework-app\django-uwsgi-nginx\app
1. If you use virtual environment, create venv befor the following step.
1. Install requirement package as below.
    ```bash
    pip install -r requirements.txt
    ```
1. Set the python interpreter.
    - click View > Command palette and select Python : select interpreter.
1. Push runserver button.(or Ctrl + F5)
1. Access to the following url.
    - http://127.0.0.1:8000/app/ 

## When you use DB backup file
1. You can use the following file for backup db.
    - django-housework-app\housework-app\django-uwsgi-nginx\app\
1. If you want to backup at 4 o'clock every day, for example, set in clonetab as following.
    - 0 4 * * * docker exec housework-app_django_1 /bin/bash -c  'cd /code/app/ && python3 backup_db.py'

# Testing (you can only use local environment)
1. You can run test after installation procedure (When you use local environment without docker).
1. Install your browser version of chrome driver from the following page.
    - https://chromedriver.chromium.org/downloads
1. Set the chrome driver into the following directory.
    - django-housework-app\housework-app\django-uwsgi-nginx\app\static\test
1. Change the following code of `tests.py`(Line:281)　please change <font color="Red">"Your chrome driver file name"</font>
    ```python
    chrome_driver = "Your chrome driver file name" if os.name == "nt" else "chromedriver"
    ```
1. Run the test.
    ```bash
    cd django-housework-app\housework-app\django-uwsgi-nginx\app
    python manage.py test
    ```
## This app test specification is in the following directory.
- django-housework-app\housework-app\django-uwsgi-nginx\app\doc

    - test_item.xlsx: test item

# Note
- This page is subject to be inaccessible or change without notice for maintenance.
- At the moment, only the Japanese version is available.
 
# Author
- mokocat
 
# License
"Housework-management-app" is under [GPL license](https://www.gnu.org/).
