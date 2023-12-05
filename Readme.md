# Claritywave challenge

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/enfasis/cw_django_dev/ec2.yml?label=Workflow)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/bd9cd7f2b3404a1b84a7bf17c1ab9d4d)](https://app.codacy.com/gh/enfasis/cw_django_dev/dashboard?utm_source=gh\&utm_medium=referral\&utm_content=\&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/bd9cd7f2b3404a1b84a7bf17c1ab9d4d)](https://app.codacy.com/gh/enfasis/cw_django_dev/dashboard?utm_source=gh\&utm_medium=referral\&utm_content=\&utm_campaign=Badge_coverage)

Author: CW-TEAM

# Setting up

## Local Development

### Poetry

Setting up `.venv` enviroment with poetry for python 3.11

```sh
poetry config virtualenvs.in-project true
pyenv local 3.11.0
poetry shell 
poetry install 
```

This project uses `ruff` as a formatter and linter

```sh
ruff check . --fix
ruff format .
```

### Testing

They are found in the `./tests/` path.

```sh
pytest
```

### Database

Sqlite for local developemen and test

## Production

Kubernetes configurations files are defined in `./deploy/`.

### Commands

Use the following example to create dummy data:

```sh
python manage.py create_dummy_data
```

It'll help you to setup two users
| username | pass |
|----------|------|
| user\_1   | 123  |
| user\_2   | 123  |

There is a command to update the ranking of the questions that are no longer of the current day

```sh
python manage.py update_daily_ranking
```

### About the strategy to solve the daily ranking

There so many ways to approach this problem, I could setup a unix cron job, django celery beat, update the ranking on every request with a background task, but I decided to make it part of the kubernetes deployment using its cronjob resource. I do believe that making optimistic updateds in an frequent interval doesn't impact the database, I probably should make and index with `created` and `is_from_today`.

### About the current deployment

This project is deployed in an EC2 Instance running kubernetes cluster using [minikube](https://minikube.sigs.k8s.io/docs/) with a Postgres Database.
There are some security group rules to access the kubernetes cluster server and the app deployed. Given that this is a toy deployment there are some security and best practices concerns, i.e., `minikube` is not for production, but for now, it gets the job done.

For learning purposes I decided to go for this approach instead of using docker swarm or just deploy the app on bare metal. Also this a list of this to improve:

*   CI

-   Make a better github action ci to reuse the docker cache from previous jobs
-   Set up rules to run specific jobs based on branches o releases
-   Test workflow to use a postgress db
-   Load testing
-   E2E

*   CD

-   Set up manual deployments, that requires approvals
-   Integrate a real GitOps strategy with... maybe... "argocd"
-   Analysis and monitor tools

*   APP

-   Django is a nice web framework, but if my views have some interaction with apis (to monitor or performance), I will consider decoupling the frontend from it.

-   For the previous reason mentionen above I used `django-ninja` instead of `rest-framework`, but I'll choose a typed library if I will interact with too many developers or I'll update the app the next year.

### About tasks

An effort list recollection, `gitops` is my weak point, since I implemented it on the fly, anyway it was a nice weekend.
| task                           | effort  |
|--------------------------------|---------|
| application analysis           | 2h      |
| application fix                | 3h      |
| application tests              | 3h      |
| ci                             | 8h      |
| cd (Learning is a fun process) | 12h 🤓☝ |

### Play with it

You can interact with it here: [DEPLOYED APP](http://184.73.145.237/), you can use any of this users:
| username | pass |
|----------|------|
| user\_1   | 123  |
| user\_2   | 123  |

**Also the cron job that update the ranking is creating a question every two minutes.**

For security reasons I'll not provide access to ec2 where this is app deployed, but I'll share some terminal text related to this deployment:

```
ubuntu@ip-172-31-85-44:~$ docker ps
CONTAINER ID   IMAGE                                 COMMAND                  CREATED        STATUS        PORTS                                                                                                                        NAMES
674531872cbd   nginx:latest                          "/docker-entrypoint.…"   3 hours ago    Up 3 hours                                                                                                                                 nginx-base
b89d7243f2e8   gcr.io/k8s-minikube/kicbase:v0.0.42   "/usr/local/bin/entr…"   11 hours ago   Up 11 hours   0.0.0.0:32797->22/tcp, 0.0.0.0:32796->2376/tcp, 0.0.0.0:32795->5000/tcp, 0.0.0.0:32794->8443/tcp, 0.0.0.0:32793->32443/tcp   minikube
ubuntu@ip-172-31-85-44:~$
```

```
ubuntu@ip-172-31-85-44:~$ kubectl get deploy
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
cw-base    1/1     1            1           50m
postgres   1/1     1            1           4h52m
```

```
ubuntu@ip-172-31-85-44:~$ kubectl get po
NAME                       READY   STATUS      RESTARTS   AGE
cw-base-6cf85f7c89-9gr7r   1/1     Running     0          51m
cw-cron-28361524-9zwff     0/1     Completed   0          18s
postgres-58488bc-rvpmg     1/1     Running     0          4h52m
```

```
ubuntu@ip-172-31-85-44:~$ kubectl get job
NAME               COMPLETIONS   DURATION   AGE
cw-cron-28361524   1/1           6s         21s
```
