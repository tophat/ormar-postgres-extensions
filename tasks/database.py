import os

from invoke import task

from .utils import ctx_run


@task()
def local_db(ctx):
    """
    Run the database for local testing
    """
    ctx_run(ctx, "docker-compose up -d")


@task()
def local_db_stop(ctx):
    """
    Stop the database stared by inv local_db
    """
    ctx_run(ctx, "docker-compose down")
