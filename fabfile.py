from fabric import task
from patchwork.transfers import rsync
from invoke import run

exclude_dirs = [".git", "node_modules", ".cache", ".github", "db.sqlite3"]


@task
def reinit(ctx):
    run("rm db.sqlite3")
    run("python manage.py migrate")
    run("python populate.py")


@task
def test(c):
    run(" coverage run manage.py test --failfast")
    run("coverage report -m ")


@task
def log(ctx):
    run("pip-compile requirements.in -o requirements.txt")

