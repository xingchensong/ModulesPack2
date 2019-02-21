# -*- coding: utf-8 -*-
# File: group.py

from contextlib import contextmanager
from time import time as timer
from utils import mylogger as logger
from utils.utils import humanize_time_delta
import six

from .base import Module


if six.PY3:
    from time import perf_counter as timer  # noqa

__all__ = ['Modules']


class ModuleTimeLogger(object):
    def __init__(self):
        self.times = []
        self.tot = 0

    def add(self, name, time):
        self.tot += time
        self.times.append((name, time))

    @contextmanager
    def timed_Module(self, name):
        s = timer()
        yield
        self.add(name, timer() - s)

    def log(self):

        """ log the time of some heavy Modules """
        if self.tot < 3:
            return
        msgs = []
        for name, t in self.times:
            if t / self.tot > 0.3 and t > 1:
                msgs.append(name + ": " + humanize_time_delta(t))
        logger.logger.info(
            "Modules took {:.3f} sec in total. {}".format(
                self.tot, '; '.join(msgs)))


class Modules(Module):
    """
    A container to hold all Modules, and trigger them iteratively.
    Note that it does nothing to _run.
    """

    def __init__(self, modules):
        """
        Args:
            modules(list): a list of :class:`Module` instances.
        """
        # check type
        for module in modules:
            assert isinstance(module, Module), module.__class__
        self.modules = modules

    def get_modules(self):
        return self.modules
