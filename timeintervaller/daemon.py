# coding: utf-8
import logging
from optparse import make_option
from django.core.management.base import BaseCommand


class BasePeriodDaemon(BaseCommand):
    log = logging.getLogger(__name__)
    option_list = BaseCommand.option_list + (
        make_option('--daemon', dest='daemon', action="store_true", default=False, help="Run as daemon"),
    )

    def log_init(self, *args, **options):
        verbosity_level_mapping = {
            1: logging.INFO,
            2: logging.DEBUG,
        }
        level = verbosity_level_mapping.get(int(options['verbosity']), logging.ERROR)
        self.log.setLevel(level)

        handler = self.log.handlers[0]
        formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        log_filename = options.get('log')
        if log_filename:
            handler = logging.handlers.TimedRotatingFileHandler(filename=log_filename, when='D', interval=1, backupCount=5)
            self.log.addHandler(handler)

    def handle(self, *args, **options):
        self.log_init(*args, **options)
        while True:
            self.handle_each_time(*args, **options)
            if not options['daemon']:
                break
