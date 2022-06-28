## Prerequisites

- Python : [link](https://www.python.org/)

## Install

Git clone

```bash
git clone https://github.com/GaetanPcht/projetthematique.git
```

```bash
cd projetthematique
```

```bash
pip install django
```

```bash
pip install djangorestframework
```

## Usage

Run this application

```bash
python manage.py runserver
# or
py manage.py runserver
```
Administrator interface

```bash
127.0.0.1:8000/admin (root:root)
```

Get JSON with stop parameter

```bash
127.0.0.1:8000/gtfs-to-json/<stop name> 
(ex : 127.0.0.1:8000/gtfs-to-json/UPJV SAINT-LEU)
```


Get JSON with stop and time parameters (shows upcoming stops within 1.5hours after the specified time)

```bash
127.0.0.1:8000/gtfs-to-json/<stop name>/YYYYMMDD-hh:mm:ss
(ex : 127.0.0.1:8000/gtfs-to-json/UPJV SAINT-LEU/20220330-14:00:00)
```


Update database
```bash
python manage.py update_db
```

## Error cases

### No database

If you don't have database. Remove folder migration then do the following command lines.

```bash
py manage.py makemigrations
# or
python manage.py makemigrations
```

```bash
py manage.py migrate
# or
python manage.py migrate
```

### Module not found

If a module is not found. Do the following command lines.

```bash
pip install <nameModule>
```

## Contributors

👨 **Gaétan PICHOUT**
- Github : [@GaetanPcht](https://github.com/GaetanPcht)

👨 **Loïc MALVOISIN**
- Github : [@malvoisinl](https://github.com/malvoisinl)

👨 **Théo METEYER**
- Github : [@tmeteyer](https://github.com/tmeteyer)

👨 **Rémy POTTIEZ**
- Github : [@Draclight](https://github.com/Draclight)
