import keyboard
from pynput.keyboard import Controller
import time
from mss import mss
import hashlib
from datetime import datetime

# life is made a lot easier by using this 
def press_key(key, mode='press'):
	if keyboard.is_pressed('q') == True:
		return

	time.sleep(0.15)
	
	if mode == 'press':
		print(f'pressed: {key}')
		return keyboard.press_and_release(key)
	elif mode == 'hold':
		print(f'held: {key}')
		return keyboard.press(key)
	elif mode == 'release':
		print(f'released: {key}')
		return keyboard.release(key)
	else:
		print('unrecognized mode')
		return

# frequently used keystrokes
def alt_tab():return press_key('alt+tab')
def alt_d():  return press_key('alt+d')
def ctrl_a(): return press_key('ctrl+a')
def ctrl_c(): return press_key('ctrl+c')
def ctrl_v(): return press_key('ctrl+v')
def enter():  return press_key('enter')

def write_text(text, url=False):
	time.sleep(0.2)
	if url:
		text = f'https://www.humblebundle.com/membership/{text}'
	print(f'wrote: {text}')
	return Controller().type(text)

def format_month(url):
	month, year = url.split('-')
	return f'{month.capitalize()} {year}:'

# wait for a change on the screen within a certain region
# used to detect when a webpage updates
def detect_change():
	sct = mss()
	region = {'top': 300, 'left': 300, 'width': 200, 'height': 200}

	print("scanning...")
	previous_hash = None

	while True:
		if keyboard.is_pressed('q') == True:
			return

		img = sct.grab(region)

		current_hash = hashlib.md5(img.rgb).hexdigest()

		if previous_hash and current_hash != previous_hash:
			print('change detected!')
			time.sleep(0.5)
			return

		previous_hash = current_hash
		time.sleep(0.15)

def iterate_url(current_url):
	months = [
		'january', 'february', 'march', 'april',
		'may', 'june', 'july', 'august',
		'september', 'october', 'november', 'december'
	] 

	month, year = current_url.split('-')
	month_index = months.index(month)
     
	# if month is december: reset index and iterate year
	if month_index == 11:
		month_index = 0
		year = int(year) + 1
	else:
		month_index += 1
  
	return f'{months[month_index]}-{year}'

def	main():
	print('initialized.')
	print('make sure you have clicked into your programs in the following order:')
	print('terminal (this one) < browser < notepad')
	print()
	print('basically you want to be able to have it so that alt+tab goes to BROWSER, and alt+double tab goes to TEXT EDITOR')
	print()
	print('hold "q" if you ever need to abort the program')
	print('Press "ENTER" to continue.')
	
	keyboard.wait('enter')
	time.sleep(0.7)

	# this will be the oldest URL from humble bundle and iterate forward
	current_url = 'december-2019'

	# get the current month and year as a string
	today = datetime.now()
	this_month = f'{today.date():%B}'.lower()
	this_year = f'{today.date():%Y}'
	end_url = f"{this_month}-{this_year}"
	first_loop = True

	while True:
		# break the loop if user wants to quit
		if keyboard.is_pressed('q') == True:
			print('"q" held: stopping program...')
			break

		# alt tab back into browser
		alt_tab()
		time.sleep(0.2)
		if first_loop == True:
			press_key('ctrl+t')
		alt_d()
		write_text(current_url, url=True)
		enter()

		# wait for page to load
		detect_change()	

		# get all games from that page
		ctrl_a()
		time.sleep(0.2)
		ctrl_c()

		if first_loop == True:
			print('first_loop = true!')

			press_key('alt', 'hold')
			press_key('tab')
			press_key('tab')
			press_key('alt', 'release')
		else:
			print('first_loop = false!')

			alt_tab()
	
		# document what section the games were taken from
		write_text(format_month(current_url))
		enter()
		# paste games in text editor
		ctrl_v()
		
		if current_url != end_url:
			current_url = iterate_url(current_url)
		else:
			break

		# for notepad formatting
		enter()
		enter()

		first_loop = False
		
	print('done.')
	return

main()