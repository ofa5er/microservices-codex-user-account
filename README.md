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

## Step1 - Building the microservice using TDD

### Initialize Django Rest Framework (DRF)

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

### Create the REST API app

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

## Step2 - Containerizing a Django Microservices
