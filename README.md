# Data_Practice

[API Document](https://www.notion.so/API-Document-c8da6497d21b43a28d7a8fef69af8c89)

1. install requiements.txt in
```
pip install -r requirements.txt
```

2. add secrets.json (Base Directory)
```
{
    "SECRET_KEY" : "secret_key",
    "DATABASES" : {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "db_name",
            "USER": "db_user",
            "PASSWORD": "db_password",
            "HOST": "db_host"
        }}
}
```

3. run manage.py
```
python manage.py runserver
```
