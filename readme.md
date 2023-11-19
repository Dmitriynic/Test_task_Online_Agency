<h2 align="center">Test task Online Agency</h2>
<p align="center">
   <img src="https://github.com/Dmitriynic/Test_task_Online_Agency/blob/main/img1.png" alt="pict" height="200" width="800">
</p>
<p align="center">
   <img alt="Static Badge" src="https://img.shields.io/badge/Python-3.9.6-red">
   <img alt="Static Badge" src="https://img.shields.io/badge/Django-4.2.7-blue">
   <img alt="Static Badge" src="https://img.shields.io/badge/djangorestframework-3.14.0-blue">
   <img alt="Static Badge" src="https://img.shields.io/badge/psycopg-3.1.13-blue">
   <img alt="Static Badge" src="https://img.shields.io/badge/License-MIT-green">
</p>

## Task 

1. update_autoru_catalog Path:
<ul>
    <li>The 'update_autoru_catalog' path should collect brands and models
    of cars from the <a href="https://auto-export.s3.yandex.net/auto/price-list/catalog/cars.xml">auto.ru</a>
     catalog and store them in the database.
    </li>
    <li>Two database models are required: Mark and Model. The Model should
    have a foreignkey referencing the Brand.</li>
    <li>It is sufficient to implement the database using SQLite.</li>
    <li>Upon each invocation of 'update_autoru_catalog', the previous data in the
    database should be deleted, and new data should be loaded.</li>
    <li>Mark values should be extracted from the "mark" tag, specifically from the
    "name" attribute (e.g. '<mark name="Thrairung"> should yield "Thairung").</li>
    <li>Model values should be extracted from the "folder" tag, specifically from the
    "name" attribute, up to the comma(e.g. '<folder name="Transformer, II" id="23666273">' should yield
    "Transformer").</li>
    <li>There should be approximately 350 marks and over 3500 models.</li>
</ul>

2. Main Page:
<ul>
    <li>Display a form on the main page allowing the selection of a brand.</li>
    <li>In response, the form should display the models associated with that brand.</li>
    <li>Design is not crucial, but Bootstrap should be included.</li>
</ul>

## Solve

###### Main info: please use '''python manage.py update_autoru_catalog''' to update database.

Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

With the virtual environment active, install Django:
```
pip install Django
```

Install psycopg 3. psycopg 3 is a package that will allow Django to 
use the PostgreSQL database that we just configured.
```
pip install "psycopg[binary]"
```

Start a Django project:
```
django-admin startproject cars
```

Edit the section "DATABASES":
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': 'cars_service',
        },
    }
}
```

Create connection service file ".pg_service.conf" with the following content:
```
[cars_service]
dbname=postgres
user=postgres
host=localhost
port=5432
```

Set global variable to the path(windows):
```
setx PGSERVICEFILE "full_path_to_your_file\.pg_service.conf"
```

Create the password file ".pg_pass.conf" with the following content:
```
localhost:5432:postgres:postgres:0000
```

Set global variable to the path:
```
setx PGPASSFILE "full_path_to_your_file\.pg_pass.conf"
```

Perform migrations:
```
python manage.py makemigrations
python manage.py migrate
```

Create an administrative account:
```
python manage.py createsuperuser
(Username: user1, password: 0000)
```

Run django server:
```
python manage.py runserver
```

Connect Django Flatpages and sites:

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
]
```

Change urls.py:
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
]
```

Add this to MIDDLEWARE in settings.py:
```
'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
```

Create templates/flatpages/default.html using ready-made css style files from:
static/css/styles.css https://startbootstrap.com/template/bare.
Move index.html to templates/flatpages/ and remove: default.html

To load styles from a folder static add followtin content to setting.py:
```
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
```

```
Import os module in setting.py
import os
```

And edit 'DIRS' in TEMPLATES:
```
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

Define a new FlatPageAdmin in fpages/admin.py to see all registered fields:
```
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
 
# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
```

And add new app to INSTALLED_APPS in setting.py:#
```
INSTALLED_APPS = [
    # ...
'fpages',
    # ...
]
```

Start new app with:
```
python manage.py startapp markmodel
```

Add new app to INSTALLED_APPS in settings.py:
```
INSTALLED_APPS = [
    # ...
    'markmodel'
    # ...
]
```

Make 2 models in markmodel/model.py using ORM(Object Related Mapping)
```
from django.db import models

class CarMark(models.Model):
    name = models.CharField(max_length = 255)

class CarModel(models.Model):
    name = models.CharField(max_length = 255)
    mark_id = models.ForeignKey(CarMark, on_delete = models.CASCADE)
```

Register models in markmodel/admin.py:
```
from django.contrib import admin
from .models import CarMark, CarModel

admin.site.register(CarMark)
admin.site.register(CarModel)
```

Again perform migrations.

Create makmodel/management/commands/update_autoru_catalog.py to delete past data from the database and load new ones.
This file parses xml and updates database.

Install requests:
```
pip install requests
```

Run this command when you need to update the database:
```
python manage.py update_autoru_catalog
```

Let's use a DjangoRestFramework.
```
pip install DjangoRestFramework
```
```
INSTALLED_APPS = [
    # ...
    'rest_framework',
    # ...
]
```

Use serializers and modelviewset to handle requests for a list of models.
In markmodel/serializers.py:
```
from rest_framework import serializers
from .models import CarMark, CarModel

class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ['id', 'name']

class CarModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'mark_id']
```

In markmodel/views.py:
```
from rest_framework import viewsets
from django.shortcuts import render
from .models import CarModel, CarMark
from .serializers import CarModelSerializer, CarMarkSerializer

class CarMarkViewSet(viewsets.ModelViewSet):
    queryset = CarMark.objects.all()
    serializer_class = CarMarkSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CarMarkSerializer(queryset, many=True)
        context = {'marks': serializer.data}
        return render(request, 'markmodel/cars.html', context)

class CarModelViewSet(viewsets.ModelViewSet):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()

    def get_queryset(self):
        mark_id = self.request.query_params.get('mark_id')
        if mark_id:
            queryset = CarModel.objects.filter(mark_id=mark_id)
        else:
            queryset = CarModel.objects.all()
        return queryset
```

Add router and path in urls.py:
```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from .views import CarMarkViewSet, CarModelViewSet

router = DefaultRouter()
router.register(r'marks', CarMarkViewSet, basename='carmark')
router.register(r'models', CarModelViewSet, basename='carmodel')

urlpatterns = [
    path('', lambda request: redirect('carmark-list'), name='home'),  # Перенаправление на список марок
    path('', include(router.urls)),
]
```

Also add html logic:
<ul>
    <li>Form for selecting car marks.</li>
    <li>model list container for displaying car models.</li>
    <li>JS file "script.js" linked for additional scripting.</li>

And js logic:
<ul>
    <li>Listens for DOMContentLoaded event.</li>
    <li>Fetches car models on car mark selection.</li>
    <li>Updates the model list dynamically.</li>
    <li>Error handling for fetch requests.</li>
