# Tutorial Django
This application runs a website with a model trained to predict prices from real estate data.

The website is built with Django and the model is trained with scikit-learn.

The goal of this project is to show how to build a website with Django and how to use a trained model to make predictions.

The model is based on the api version of the project [immo-app](https://github.com/DeLeb86/immo-app) and try to extend it.

## How to use it

The only purpose of the code in this branch and others, is to give you exemples. You can use it if you are stuck or if you want to see how to do something.

Only the readme is necessary to create the project.

They are two parts in this project:
1. Create a simple page with a form than the user can fill in.
2. Use the data from the form to make a prediction with a trained model and display the result.

## APP

### install and run

First, you need to clone the immo-app project to get the data and the model. You can find it [here](https://github.com/DeLeb86/immo-app)

Then on another folder, you will create the Django project.

Create a virtual environment and activate it.

```bash
python -m venv venv
```

for windows cmd.exe
```bash
venv\Scripts\activate.bat
```

for windows PowerShell
```bash
venv\Scripts\Activate.ps1
```

for linux and MacOS
```bash
source venv/bin/activate
```

Then install Django and the other packages.

with the requirements.txt file in this project
```bash
pip install -r requirements.txt
```

or with the following commands

```bash
pip install django
pip install scikit-learn
pip install pandas
pip install numpy
pip install fastapi
```

Then you can create the project and the app.

```bash
django-admin startproject django_tuto
cd django_tuto
python manage.py startapp estimate
```

You know have the project and the app.

You can true to run the server with the following command.

```bash
python manage.py runserver
```

You can now go to the address [http://localhost:8000/](http://localhost:8000/) and you should see the Django welcome page.

We will now create our first page.

## Create the first page

We will add the "estimate" app to the installed apps in the settings.py file.

```python
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'estimate',
]
```

We will go in the "estimate" app and open the file called views.py.
There, we will create a function that will return a simple page.

```python
from django.shortcuts import render
from django.http import HttpResponse

def mainPage(request):
	return HttpResponse('<h1>Home</h1>')
```

Then we will create a route to this page. We will go in the "django_tuto" folder and open the file called urls.py.
We will add the following code.

```python
from django.urls import path

from estimate import views

urlpatterns = [
	path('', views.mainPage, name='mainPage'),
]
```

Now if you go to the address [http://localhost:8000/](http://localhost:8000/), you should see the "Home" title.

Congratulations, you have created your first page with Django. Amazing, isn't it?

#### Explanation

The function mainPage is a view. It takes a request as a parameter and return a response. In this case, the response is a simple string with the title "Home".

The urls.py file is used to create the routes of the website. It is a list of paths. Each path is a tuple with a string, a function and a name. The string is the path of the page, the function is the view and the name is the name of the path.


## Create a form

We will now create a form that the user can fill in. We will go in the "estimate" app and create a file called forms.py.
We will add the following code.

```python
from django import forms

class PropertyForm(forms.Form):
    PostalCode = forms.IntegerField(label="Postal Code", min_value=1000, max_value=9999)
    TypeOfProperty = forms.ChoiceField(label="Type of Property", choices=[(0, "House"), (1, "Apartment")])
    TypeOfSale = forms.ChoiceField(label="Type of Sale", choices=[(0, "Normal"), (1, "Auction")])
    Kitchen = forms.ChoiceField(label="Kitchen", choices=[("installed", "Installed"), ("usa installed", "USA Installed"), ("semi equipped", "Semi Equipped"), ("usa semi equipped", "USA Semi Equipped"), ("hyper equipped", "Hyper Equipped"), ("usa hyper equipped", "USA Hyper Equipped")], required=False)
    StateOfBuilding = forms.ChoiceField(label="State of Building", choices=[("to be done up", "To be done up"), ("to restore", "To restore"), ("to renovate", "To renovate"), ("good", "Good"), ("just renovated", "Just renovated"), ("as new", "As new")], required=False)
    Bedrooms = forms.IntegerField(label="Number of Bedrooms", min_value=0, max_value=10, required=False)
    SurfaceOfGood = forms.FloatField(label="Surface of Good", min_value=0, max_value=10000, required=False)
    NumberOfFacades = forms.IntegerField(label="Number of Facades", min_value=0, max_value=10, required=False)
    LivingArea = forms.FloatField(label="Living Area", min_value=0, max_value=10000)
    GardenArea = forms.FloatField(label="Garden Area", min_value=0, max_value=10000, required=False)

```

Then we will go in the "estimate" app and open the file called views.py.
We will modify the mainPage function to return a form.

```python
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PropertyForm

def mainPage(request):
	form = PropertyForm()
	return render(request, 'estimate/mainPage.html', {'form': form})
```

Then we will create a folder called "templates" in the "estimate" app. In this folder, we will create a file called "mainPage.html".
We will add the following code.

```html	
<!DOCTYPE html>
<html>
<head>
	<title>Estimation</title>
</head>
<body>
	<h1>Estimation</h1>
	<form method="POST">
		{% csrf_token %}
		{{ form.as_p }}
		<button type="submit">Submit</button>
	</form>
</body>
</html>
```

Now if you go to the address [http://localhost:8000/](http://localhost:8000/), you should see a form with the fields we have created.


#### Explanation

The forms.py file is used to create a form. It is a class that inherits from forms.Form. Each field of the form is an attribute of the class. The attribute is an instance of a class that inherits from forms.Field.

The views.py file is used to create a view. It is a function that takes a request as a parameter and return a response. In this case, the response is a form. The form is created with the form we have created in the forms.py file. We use the render function to return a template with the form.

## Use the form to make a prediction and display the result

We will now use the data from the form to make a prediction with a trained model and display the result. We will go in the "estimate" app and open the file called views.py.

We will modify the mainPage function to use the data from the form to make a prediction and display the result.

I will use the model and the encoders from the immo-app project. You can use your own model instead.

```python

# imports for the prediction
import pandas as pd
import numpy as np
import json,pickle
from fastapi.encoders import jsonable_encoder
from regression.features import feature_engineering
from regression.preprocessing import encode_dataframe
import os

# imports for django
from django.shortcuts import render

from .forms import PropertyForm


def mainPage(request):
	# if the request is a GET request
    if request.method == "GET":
        form = PropertyForm()
        return render(request, "main.html", {"form": form})
    
	# if the request is a POST request
    form = PropertyForm(request.POST)

	# if the form is not valid
    if not form.is_valid():
        return render(request, "main.html", {"form": form})
    
	# if the form is valid
    config=json.load(open("resources/config.json"))

    model=pickle.load(open(config['model_path'],"rb"))
    encoder_struct=pickle.load(open(config["encoder_path"],"rb"))
    print("model and encoders loaded!")
    data = {
        "PostalCode": form.cleaned_data["PostalCode"],
        "TypeOfProperty": form.cleaned_data["TypeOfProperty"],
        "TypeOfSale": form.cleaned_data["TypeOfSale"],
        "Kitchen": form.cleaned_data["Kitchen"],
        "StateOfBuilding": form.cleaned_data["StateOfBuilding"],
        "Bedrooms": form.cleaned_data["Bedrooms"],
        "SurfaceOfGood": form.cleaned_data["SurfaceOfGood"],
        "NumberOfFacades": form.cleaned_data["NumberOfFacades"],
        "LivingArea": form.cleaned_data["LivingArea"],
        "GardenArea": form.cleaned_data["GardenArea"],
    }
    df=pd.DataFrame.from_dict(jsonable_encoder(data),orient="index").transpose()
    df=df.reindex(columns=["PostalCode"]+model.feature_names_in_.tolist())
    df=feature_engineering(df)
    df.drop("PostalCode",axis=1,inplace=True)
    df,e=encode_dataframe(df,encoder_struct)
    score=np.abs(model.predict(df))
	
    return render(request, "main.html", {"form": form, "estimation": str(score[0])})
```

You should see the result of the prediction on the page.

That's it, you have created a website with Django and used a trained model to make predictions.

In the second part, we will see how to create authentication and how to work with a database.

To view the code to the second part, explore the branch "part2" of this project.

Otherwise, you can continue with the following instructions.

## Part 2

Welcome to the part 2 of the Django tutorial. In this part, we will learn about the Django models and how to use them to create a database for our web application. Also, we will learn about the Django authentication system and how to use it to create a login and registration system for our web application.

## Django Models
Django models are used to create a database for our web application. A model is a class that represents a table in the database. Each attribute of the model represents a column in the table. Django models are defined in the `models.py` file of the application.

Django use an Object-Relational Mapping (ORM) to interact with the database. This means that we can use Python code to interact with the database instead of SQL queries.

To create a model, we need to define a class that inherits from the `django.db.models.Model` class. Each attribute of the model represents a column in the table. The type of the attribute represents the type of the column. For example, the `CharField` type represents a `VARCHAR` column in the database. You can refer to the official [Django documentation](https://docs.djangoproject.com/en/3.2/ref/models/fields/) to see the list of all available field types.

During this part, I will give you urls to the official documentation and tasks but not directly the code in the readme. You can check the code in the project but try to do it yourself first.

### Preparation
Before we start, you may have seen an error in the terminal `You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.`

This error is because we have created a new application but we haven't applied the migrations yet. To apply the migrations, run the following command in the terminal:
```bash
python manage.py migrate
```

Apply the migrations means to create the tables in the database for the models we have created. The `migrate` command is used to apply the migrations.

When you will change the models, you will need to create a new migration and apply it. To create a new migration, run the following command in the terminal:
```bash
python manage.py makemigrations
```

Then create a superuser:
```bash
python manage.py createsuperuser
```
Follow the instructions and create a superuser.


### Task 1
Create a login page.

I will take a shortcut here. You can check the official documentation [here](https://docs.djangoproject.com/en/3.2/topics/auth/default/#using-the-views) to see how to create a login page. 

In the `urls.py` file create this path:
```python
path("accounts/login/", auth_views.LoginView.as_view(template_name='admin/login.html', extra_context={         
              'title': 'Login',
              'site_title': 'Tuto',
              'site_header': 'Tuto'}), name="login"),
```

Now, in the function `mainPage` in the `views.py` file, add this:
```python
from django.contrib.auth.decorators import login_required
@login_required
def mainPage(request):
	...
```

Try to access the main page, you will be redirected to the login page. You can use the superuser you have created to login.

### Task 2
Create a model for your estimations.

Create a new model in the `models.py` file. For details, you can check the official documentation [here](https://docs.djangoproject.com/en/3.2/topics/db/models/).

### Task 3
Modify the `mainPage` function to save the new estimations.
Modify the `mainPage` function to get and display the old estimations

Check the official documentation [here](https://docs.djangoproject.com/en/3.2/topics/db/queries/).

### Task 4
Modify the template to display the old estimations.

Good luck! If you have any questions, feel free to ask me. I will be happy to help you.