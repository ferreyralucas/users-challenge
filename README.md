### Steps to run the project:

1. Define environment files
```
cp env.local .env
```

2. Copy the local Django settings file:
```
cp config/settings/dev.local.py config/settings/dev.py
```

3. Install pre-commit githooks:
```
pre-commit && pre-commit install
```

4. Build and run the project:
```
docker-compose up
```

# That's it!


### To load the database dump:

```
python manage.py migrate
python manage.py loaddata data.json
```

##### Access to the Swagger interface

```
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```
