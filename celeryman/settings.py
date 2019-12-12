import os

from celery.schedules import crontab

from chassis.settings import *  # noqa: F403

SERVICE_NAME = SERVICE_CONF.name  # noqa: F405
SERVICE_NAMESPACE = SERVICE_CONF.namespace  # noqa: F405

ROOT_URLCONF = f'{SERVICE_NAME}.urls'

SERVICE_DOCKERFILES = {
    '': [
        'chassis.dockerfile.BASE_IMAGE',
        'chassis.dockerfile.DJANGO_SETTINGS_ENV',
        'chassis.dockerfile.PIP_INSTALL',
        'chassis.dockerfile.COPY_SERVICE',
        'chassis.dockerfile.COLLECTSTATIC',
    ]
}

SERVICE_FEATURES = {
    # Default features for most services:

    'database': {
        'cls': 'chassis.features.Postgres'
    },
    'manage': {
        'cls': 'chassis.features.Manage',
        'depends_on': ['database']
    },
    'tests': {
        'cls': 'chassis.features.PyTest',
        'depends_on': ['database']
    },
    'web': {
        # default backend setup has nginx as a reverse proxy to a uwsgi based python service.
        # You can override the default resource settings for these pods here.  'nginx' for the
        # reverse proxy and 'kubernetes' for the uwsgi pod.
        #
        # more information is available at:
        #    http://devdocs.platform-dev.gcp.oreilly.com/chassis/features.html#setting-kubernetes-resources
        #
        # 'nginx': {
        #     'dev-gke': {
        #         'replicas': 1,
        #         'resources': {
        #             'requests': {'cpu': '100m', 'memory': '75Mi'},
        #             'limits': {'cpu': '250m', 'memory': '150Mi'}
        #         }
        #     },
        #     'prod-gke': {...}
        # },
        'cls': 'chassis.features.Http',
        'depends_on': ['database']
    },
    'dredd': {
        'cls': 'chassis.features.Dredd',
        'dockerfile': 'dredd',
        'api_feature': 'web'
    },
    "celery": {
        "cls": "chassis.features.Celery",
        "depends_on": ["database", "redis"],
        "kubernetes": {
            "replicas": 2,
            "resources": {
                "requests": {"cpu": "250m", "memory": "250Mi"},
                "limits": {"cpu": "500m", "memory": "375Mi"},
            },
        },
    },
    "redis": {
        "cls": "chassis.features.Redis",
        "docker_compose": {"image": "redis:3.2"},
    },
    "celerybeat": {
        "cls": "chassis.features.CeleryBeat",
        "depends_on": ["database", "redis"],
        "kubernetes": {
            "resources": {
                "requests": {"cpu": "64m", "memory": "64Mi"},
                "limits": {"cpu": "128m", "memory": "128Mi"}
            }
        }
    },
    "consumers": {
        "cls": "chassis.features.Consumers",
        "depends_on": ["database", "redis"],
        "kubernetes": {
            "replicas": 1,
            "resources": {
                "requests": {"cpu": "250m", "memory": "250Mi"},
                "limits": {"cpu": "500m", "memory": "375Mi"}
            }
        }
    },
}

INSTALLED_APPS += [  # noqa: F405
    SERVICE_NAME
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_TEST_NAME') or os.environ.get('DB_NAME', SERVICE_NAME),
        'USER': os.environ.get('DB_USER', SERVICE_NAME),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'database'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'CONN_MAX_AGE': os.environ.get('DB_CONN_MAX_AGE', 60),
        'TEST': {
            'NAME': os.environ.get('DB_TEST_NAME', f'test_{SERVICE_NAME}'),
        }
    }
}

JWT_ENABLED = True

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")

CELERY_WORKER_DISABLE_RATE_LIMITS = True
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TASK_TIME_LIMIT = 23 * 60 * 60  # 23 hours

CELERY_TASK_ALWAYS_EAGER = True

# CELERY_BEAT_SCHEDULE = {
#     "fetch_avatar_urls": {
#         "task": "celeryman.tasks.fetch_avatar_urls",
#         "schedule": crontab(minute="*/1")
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

CELERYMAN_WORK_CUD_ROUTING_KEY = f"magpie.work.*.{ENV}"
CELERYMAN_MAGPIE_WORK_CUD_QUEUE = (
    f"Celeryman-magpie-work-CUD-{ENV}"  # noqa: F405
)


# DEFAULT_CONSUMER_BROKER = [
#     'amqp://certifications_service:f1ef0a4f5e5785e513e4d27f97d86bbf@rabbitmq-0.platform-prod.gcp.oreilly.com:5672',
#     'amqp://certifications_service:f1ef0a4f5e5785e513e4d27f97d86bbf@rabbitmq-1.platform-prod.gcp.oreilly.com:5672',
#     'amqp://certifications_service:f1ef0a4f5e5785e513e4d27f97d86bbf@rabbitmq-2.platform-prod.gcp.oreilly.com:5672',
# ]
DEFAULT_CONSUMER_BROKER = "amqp://guest:guest@rabbitmq.platform:5672//"

EVENT_BROKER = DEFAULT_CONSUMER_BROKER
CONSUMER_EVENT_BROKER = DEFAULT_CONSUMER_BROKER
