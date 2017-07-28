# Tutorial - Building a microservice using Python, Django and docker

## Introduction

This is part of Microservice codeX Series.
In this part, you will learn best practices to develop a microservice using Django and Django Rest Framework (DRF).

## Requirements

In this tutorial, we are going to develop the User Account microservice. The purpose of this microservice is to store all the needed information related to the user acounts of the e-commerce website. As it is reommended in MSA, the microservice will offer a REST API that allows to:

- Create a new user
- Retrieve profile infromation related to a user
- Update profile info of a user
- Delete the user profile

## Prerequisites

### Tools

- Python 3.x is installed

- TBD

### Knowledge

- Python
- Django

## 1 - Build the microservice using TDD

### Step 1.1 - Create the initial project

Why DRF ?
TBD
DRF Requirements

Create the project folder

```bash
mkdir microservices-codex-user-account
cd microservices-codex-user-account
```

Create the virtual environment

```bash
virtualenv -p /usr/bin/python3 venv
```

Activate your virtual environment

```bash
source venv/bin/activate
```

```bash
pip install Django
```

If you don't have pip install it (TBD).

Create Django project

```bash
  django-admin startproject user_account
```
We should have now a folder with the name `user_account`

```bash
user_account
├─user_account
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

Using pip, install DRF

```bash
 pip install djangorestframework
```

We need to keep track of all the requirements of our project. We can do that by using `pip freeze`

```bash
 pip freeze > requirements.txt
```

To use DRF, we will have to add `rest_framework` into `settings.py`.

```python
# /microservices-codex-user-account/user_account/settings.py
.
.
.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Ensure a comma ends this line
    'rest_framework', # Add this line
]
```

### Step 1.2 - Create the REST API app

In this section, we are going to create a REST API since it is recommended to have an API for every microservice in MSA.

In Django, we can create multiple apps that integrate to form one application. An app in Django is simply a python package with a bunch of files including the `__ini__.py` file.

`cd` into the user_account directrory and create the API using the following command.

```bash
python manage.py startapp api
```

The command created a new app called `api`. It will hold our API logic.

To integrate our `api` app with the `user_account` main app. We'll have to add it to `settings.py` of the main app.

```python
.
.
.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api', # Add this line
]
```

### Step 1.2 - Develop the create user method

#### Create the Test

We would like to create the model of the user accounts. Before doing that we need to write some tests in the tests.py folder of our api app (TDD remember ;-) ).

Add the following code to `./api/test.py`. It imports the test case from django.test. The test case has a single test that tests whether the model can create a user account using an ID.

```python
# /api/tests.py

from django.test import TestCase
from .models import   UserAccount

class ModelTestCase(TestCase):
    """This class defines the test suite for the user_account model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.id = "qweqw121212sdasdasd"
        self.first_name = "qweqw121212sdasdasd"
        self.last_name = "qweqw121212sdasdasd"
        self.address = "qweqw121212sdasdasd"
        self.email = "qweqw121212sdasdasd"
        self.user_account = UserAccount(id=self.id)

    def test_model_can_create_a_user_account(self):
        """Test the user account model can create a user account."""
        old_count =   UserAccount.objects.count()
        self.user_account.save()
        new_count =   UserAccount.objects.count()
        self.assertNotEqual(old_count, new_count)
```

#### Define the model

We create the user account model by putting the following code `models.py`

```python
# api/models.py
from django.db import models

class   UserAccount(models.Model):
    """This class represents the user account model."""
    uid = models.CharField(max_length=255, blank=False, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    billing_address = models.CharField(max_length=255, blank=True)
    shipping_address = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
```

To propogate the changes made on the model to the database schema, Django use `migrations`

Create migrations

```bash
python manage.py makemigrations
```

Apply migrations to the Databse:

```bash
python manage.py migrate
```

##### Create the serializer

Create a Model Serializer by creating a new file in the folder `api` called `serializers.py`

```python
# api/serializers.py

from rest_framework import serializers
from .models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = UserAccount
        fields = ('uid', 'first_name', 'last_name', 'email', 'billing_addresse',
        'shipping address' , 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')

```

#### Create the Views

we write the following code in `tests.py` to test whether the API will create a user account successfully.

```python
# api/tests.py

# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.uid = {'uid': '13123aaed123123asdd'}
        self.response = self.client.post(
            reverse('create'),
            self.uid,
            format="json")

    def test_api_can_create_a_user_account(self):
        """Test the api has user account creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
```

This test will fail when we run it because we haven't implemeneted the views and the urls for handling POST request.

So, now we are going to implement them. We write on `views.py` the following code:

```python
# api/views.py
from django.shortcuts import render
from rest_framework import generics
from .serializers import UserAccountSerializer
from .models import UserAccount

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new user account."""
        serializer.save()
```

#### Handle Urls

Create a `urls.py` file on the api directory. This is where we define our url patterns.

```python
# api/urls.py
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView

urlpatterns = {
    url(r'^useraccount/$', CreateView.as_view(), name="create"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
```

Finally, we add a url to the main app `urls.py` file so that it points to our API app.
```python

# user_account/urls.py
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('api.urls')) # Add this line
]

```

#### Run

First, we will make sure that the tests are successfully executed using the following command:

```bash
python manage.py test
```

Then we run the server and enter the URL (http//127.0.0.1:8000/useraccount) in the browser.

## Step2 - Containerizing a Django Microservices
