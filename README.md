# todoProject

create file `local_settings.py`  with property
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_bd_name',
        'USER': 'user_name',
        'PASSWORD': 'user_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SECRET_KEY = 'SECRET_KEY'
```

## Other
* Code Convention. For analyzing and establishing clean code (according to PEP8) we use **pylint**.
In addition since project uses Django **pylint_django** plugin for pylint is used. All pylint
configurations are in **.pylintrc** config file. To check specific  file or package use:

    ```sh
    pylint --rcfile='path' filename.py
    ```
    Additional information: [Pylint User Manual](https://pylint.readthedocs.io/en/latest/)
