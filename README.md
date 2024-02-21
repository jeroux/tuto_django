# Tutorial Django
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