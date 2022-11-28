# Paradigms Project Group 14

# About The Project

Our project is a Python + Django application that acts as a platform to connect
recruiters to potential candidates within the technological space. The information
is stored in a database using SQLite and all that data is stored and accessed to
ensure functionality in the overall design.

## Built With
List here all the dependencies of your project (including version). For example:

* [Python 3.10.8](https://www.python.org/)
* [Django 4.1.3](https://www.djangoproject.com/)
* [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)
* [Bootstrap 4.0](https://getbootstrap.com)
* [SQLite3](https://www.sqlite.org/index.html)
* [TkInter](https://docs.python.org/3/library/tkinter.html)

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* After installing and setting up Python, install pip
  ```sh
  python -m ensurepip --upgrade
  ```

* After installing pip, install Django
  ```sh
  python -m pip install Django
  ```

* Download Django Crispy Forms
  ```sh
  pip install django-crispy-forms
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/agonza42/ParadigmsProjectGroup14.git
   ```
   
2. Create database tables
   ```sh
   python manage.py migrate
   ```
   
3. Run server
   ```sh
   python manage.py runserver
   ```
