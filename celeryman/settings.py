import os

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
        "queues": ["fast", "slow"],
        "depends_on": ["database", "redis"],
        "kubernetes": {
            "replicas": 2,
            "resources": {
                "requests": {"cpu": "250m", "memory": "250Mi"},
                "limits": {"cpu": "500m", "memory": "400Mi"},
            },
        },
    },
    "redis": {
        "cls": "chassis.features.Redis",
        "docker_compose": {"image": "redis:3.2"},
    },
    "consumers": {
        "cls": "chassis.features.Consumers",
        "depends_on": ["database", "redis"],
        "kubernetes": {
            "replicas": 2,
            "resources": {
                "requests": {"cpu": "250m", "memory": "250Mi"},
                "limits": {"cpu": "500m", "memory": "400Mi"},
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

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

CELERY_WORKER_DISABLE_RATE_LIMITS = True
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TASK_TIME_LIMIT = 23 * 60 * 60  # 23 hours
