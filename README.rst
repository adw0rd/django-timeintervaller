django-timeintervaller
=======================

A simple asynchronous task-scheduler for ``Django``. For more functionality, I recommend the use ``Celery``!

The order of entry in the pool is important! Tasks is running step-by-step.
If your task is running longer than `interval`, then the next start will be immediately after the first.

Each task is starting in new thread.

Running
---------
::

    ./manage.py timeintervallerd --daemon

Settings
----------

Please, see ``settings.py``
