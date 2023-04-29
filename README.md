Steps to run the project:

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
pre-commit install
```

4. Build and run the project:
```
docker-compose up
```

5. Load the local database dump:
```
python manage.py migrate
python manage.py loaddata data.json
```

That's it!
