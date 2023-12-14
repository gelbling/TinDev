# TinDev Platform: A Tech Recruitment Tool

## Overview

Welcome to TinDev, an innovative Python and Django-based application crafted to bridge the gap between technology recruiters and aspiring candidates. Our platform harnesses SQLite for robust data management, ensuring a seamless and efficient recruitment process.

## Core Technologies
TinDev is built upon a solid foundation of dependable and cutting-edge technologies. Key components include:

* [Python 3.10.8](https://www.python.org/) - The backbone of our application, renowned for its versatility and ease of use.
* [Django 4.1.3](https://www.djangoproject.com/) - A high-level Python web framework that encourages rapid development and clean, pragmatic design.
* [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/) - Enhances Django forms with Bootstrap styling.
* [Bootstrap 4.0](https://getbootstrap.com) - A front-end framework for developing responsive and mobile-first projects.
* [SQLite3](https://www.sqlite.org/index.html) - Our chosen database engine, known for its reliability and simplicity.
* [TkInter](https://docs.python.org/3/library/tkinter.html) - A standard Python interface to the Tk GUI toolkit.

## Getting Started

Follow these steps to set up your own local instance of TinDev.

### Prerequisites

Here's what you need to begin:

* Ensure Python is installed, then set up pip:
  ```sh
  python -m ensurepip --upgrade
  ```

* Install Django using pip:
  ```sh
  python -m pip install Django
  ```

* Get Django Crispy Forms for enhanced form styling:
  ```sh
  pip install django-crispy-forms
  ```

### Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/agonza42/ParadigmsProjectGroup14.git
   ```
   
2. Set up the database:
   ```sh
   python manage.py migrate
   ```
   
3. Start the local server:
   ```sh
   python manage.py runserver
   ```

Embark on your journey with TinDev, where technology meets talent!
