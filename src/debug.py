#import data.scoreboard_config
import time
import sys

debug_enabled = False

panel_number = '0'

def set_panel_number(num):
	global panel_number
	panel_number = str(num)

def set_debug_status(config):
	global debug_enabled
	debug_enabled = config.debug

def __debugprint(text):
	print(text)
	sys.stdout.flush()

def log(text):
	if debug_enabled:
		__debugprint("PANEL {} DEBUG ({}): {}".format(panel_number, __timestamp(), text))

def warning(text):
  __debugprint("PANEL {} WARNING ({}): {}".format(panel_number, __timestamp(), text))

def error(text):
	__debugprint("PANEL {} ERROR ({}): {}".format(panel_number, __timestamp(), text))

def info(text):
	__debugprint("PANEL {} INFO ({}): {}".format(panel_number, __timestamp(), text))

def __timestamp():
	return time.strftime("%H:%M:%S", time.localtime())
