""" Dependencies """
import time
import logging

def time_performance(fn):
	
	def wrapper(*args, **kwargs):
		t_start = time.time()
		f_output = fn(*args, **kwargs)
		t_taken = time.time() - t_start
		print('{} ran in: {} seconds'.format(fn.__name__, t_taken))
		return f_output
	
	return wrapper

def log_fn_call(fn):
	
	logging.basicConfig(filename='{}.log'.format(fn.__name__), level=logging.info)

	def wrapper(*args, **kwargs):
		logging.info('Ran with args: {}  and kwargs: {}'.format(args, kwargs))
		return fn(*args, **kwargs)
	
	return wrapper