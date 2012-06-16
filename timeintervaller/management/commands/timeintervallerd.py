# coding: utf-8
"""A simple asynchronous task-scheduler for Django.

The order of entry in the POOL is important! Tasks is shedulled step-by-step.
If your task is running longer than `interval`, then the next start will be immediately after the first.

Each task is starting in new thread.
"""

import time
import threading

from django.conf import settings

from timeintervaller.daemon import BasePeriodDaemon


class Command(BasePeriodDaemon):
    pool = tuple()

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.pool = settings.TIMEINTERVALLER_POOL
        for task in self.pool:
            target = task['target'].split('.')
            task['package'], task['module'], task['function'] = ".".join(target[:-2]), target[-2], target[-1]
            task['TTL'] = time.time()
            task['object'] = __import__("{}.{}".format(task['package'], task['module']))\
                .__dict__[task['module']]\
                .__dict__[task['function']]

    def handle_each_time(self, *args, **options):
        run_task = args[0] if args else None
        for task in self.pool:
            if run_task is not None and run_task != task['target']:
                continue
            current_time = time.time()
            if task['TTL'] < current_time:
                task['TTL'] = current_time + task['interval']
                self.log.debug('Run [{time}] task: {task}'.format(time=current_time, task=task))
                self.worker(task)

    def worker(self, task):
        def runner(task):
            self.log.info('Start task "{}"'.format(task['target']))
            task['last_result'] = task['object'](*task['args'], **task['kwargs'])
            self.log.info('End task "{}"'.format(task['target']))
        thread = threading.Thread(target=runner, args=[task])
        thread.daemon = True
        thread.start()
        return True
