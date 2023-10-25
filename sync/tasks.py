from project.celery import app

from .models import Environment, Project


@app.task(bind=True)
def update_remote_project_keys(self, project_id: int):
    project = Project.objects.prefetch_related("environments").get(pk=project_id)
    for environment in project.environments.all():
        environment.write_authorized_keys()


@app.task(bind=True)
def update_remote_env_keys(self, environment_id: int):
    environment = Environment.objects.get(pk=environment_id)
    environment.write_authorized_keys()


@app.task(bind=True)
def sync_all_projects(self):
    for project in Project.objects.all():
        update_remote_project_keys.apply_async(args=[project.pk])
