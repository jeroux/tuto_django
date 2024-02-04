# Tutorial Django
This application runs a website with a model trained to predict prices from real estate ads.

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
pip install django-crispy-forms
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


