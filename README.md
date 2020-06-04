## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Launch](#launch)

## General info
This is the repository of blog web app.
This project enables you to create either forum-structured page where authenitcated users could post, or self-blog where you as a owner may only create a posts.

Blog consists of:
* creating posts
* creating comments 
* like/unlike the posts
* like/unlike the comments
* dynamic menu
* recaptcha integration with adding comments


## Technologies
Project is created with:
* [django](https://www.djangoproject.com)
* [pipenv](https://github.com/pypa/pipenv)


## Launch
[Pipenv](https://github.com/pypa/pipenv) is a package-manager tool of the project.


1. Create appropriate directory for the project and inside generate virtual environment

```bash
$ cd ../project_directory
$ pipenv --python 3.8
```


2. Activate virtual environment, clone repository to your local machine and install depedencies from Pipfile.lock

```bash
$ pipenv shell
$ git clone https://github.com/adamjanas/full_featured_blog.git
$ pipenv install
```


3. If you need help or more informations about pipenv, run:

```bash
$ pipenv --help
```