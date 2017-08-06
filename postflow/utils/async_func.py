from flask import copy_current_request_context
from threading import Thread
from functools import wraps

def run_async(func):
	"""
		run_async(func)
			function decorator, intended to make "func" run in a separate
			thread (asynchronously).
			Returns the created Thread object

			E.g.:
			@run_async
			def task1():
				do_something

			@run_async
			def task2():
				do_something_too

			t1 = task1()
			t2 = task2()
			...
			t1.join()
			t2.join()
	"""

	@wraps(func)
	def async_func(*args, **kwargs):
		func_hl = Thread(
            target = copy_current_request_context(func),
            args = args,
            kwargs = kwargs)
		func_hl.start()
		return func_hl

	return async_func

