import functools
import json
import multiprocessing
import os
import threading
from contextlib import contextmanager
from threading import Thread
from ._colorizer import Colorizer
from ._locks_machinery import create_handler_lock

class Message(str):
    __slots__ = ('record',)

class Handler:

    def __init__(self, *, sink, name, levelno, formatter, is_formatter_dynamic, filter_, colorize, serialize, enqueue, multiprocessing_context, error_interceptor, exception_formatter, id_, levels_ansi_codes):
        self._name = name
        self._sink = sink
        self._levelno = levelno
        self._formatter = formatter
        self._is_formatter_dynamic = is_formatter_dynamic
        self._filter = filter_
        self._colorize = colorize
        self._serialize = serialize
        self._enqueue = enqueue
        self._multiprocessing_context = multiprocessing_context
        self._error_interceptor = error_interceptor
        self._exception_formatter = exception_formatter
        self._id = id_
        self._levels_ansi_codes = levels_ansi_codes
        self._decolorized_format = None
        self._precolorized_formats = {}
        self._memoize_dynamic_format = None
        self._stopped = False
        self._lock = create_handler_lock()
        self._lock_acquired = threading.local()
        self._queue = None
        self._queue_lock = None
        self._confirmation_event = None
        self._confirmation_lock = None
        self._owner_process_pid = None
        self._thread = None
        if self._is_formatter_dynamic:
            if self._colorize:
                self._memoize_dynamic_format = memoize(prepare_colored_format)
            else:
                self._memoize_dynamic_format = memoize(prepare_stripped_format)
        elif self._colorize:
            for level_name in self._levels_ansi_codes:
                self.update_format(level_name)
        else:
            self._decolorized_format = self._formatter.strip()
        if self._enqueue:
            if self._multiprocessing_context is None:
                self._queue = multiprocessing.SimpleQueue()
                self._confirmation_event = multiprocessing.Event()
                self._confirmation_lock = multiprocessing.Lock()
            else:
                self._queue = self._multiprocessing_context.SimpleQueue()
                self._confirmation_event = self._multiprocessing_context.Event()
                self._confirmation_lock = self._multiprocessing_context.Lock()
            self._queue_lock = create_handler_lock()
            self._owner_process_pid = os.getpid()
            self._thread = Thread(target=self._queued_writer, daemon=True, name='loguru-writer-%d' % self._id)
            self._thread.start()

    def __repr__(self):
        return '(id=%d, level=%d, sink=%s)' % (self._id, self._levelno, self._name)

    @contextmanager
    def _protected_lock(self):
        """Acquire the lock, but fail fast if its already acquired by the current thread."""
        if getattr(self._lock_acquired, 'value', False):
            raise RuntimeError("Lock is already acquired by the current thread")
        
        with self._lock:
            try:
                self._lock_acquired.value = True
                yield
            finally:
                self._lock_acquired.value = False

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_lock'] = None
        state['_lock_acquired'] = None
        state['_memoize_dynamic_format'] = None
        if self._enqueue:
            state['_sink'] = None
            state['_thread'] = None
            state['_owner_process'] = None
            state['_queue_lock'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._lock = create_handler_lock()
        self._lock_acquired = threading.local()
        if self._enqueue:
            self._queue_lock = create_handler_lock()
        if self._is_formatter_dynamic:
            if self._colorize:
                self._memoize_dynamic_format = memoize(prepare_colored_format)
            else:
                self._memoize_dynamic_format = memoize(prepare_stripped_format)
