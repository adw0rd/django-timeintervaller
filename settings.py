import sys

INSTALLED_APPS = (
    'timeintervaller',
    'test_app'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'timeintervaller.daemon': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'timeintervaller.daemon': {
            'handlers': ['timeintervaller.daemon'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

TIMEINTERVALLER_POOL = (
    {
        'target': 'test_app.utils.recache_statistics',
        'args': ['daily', ],
        'kwargs': {"something": 42, },
        'interval': 30 * 60,  # Every half of hour
    },
    {
        'target': 'test_app.utils.sitemap_rebuilt',
        'args': [],
        'kwargs': {},
        'interval': 5 * 60 * 60,  # Every 5 hours
    },
)
