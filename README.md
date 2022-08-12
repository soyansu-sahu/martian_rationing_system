# martian_rationing_system
This project is about a martian's ration or food based on daily requirement and provide   inputs on which packet to consume on a given day and how many days the martian will survive with the available inventory




## Run Locally


### Clone the project


```bash
  git clone https://github.com/soyansu-sahu/martian_rationing_system.git
```

### Create Environment

```bash
  python3 -m venv env_name
```
### Activate Environment(env)

```bash
  $ souce env/bin/activate
```


## Database Migrations


```bash
 $ python3 manage.py makemigrations
 $ python3 manage.py migrate
```

## Create Super User


```bash
 $ python3 manage.py createsuperuser
```

## Run Server

```bash
$ python3 manage.py runserver
```
