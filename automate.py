import keyboard
from pynput.keyboard import Controller
from pynput.mouse import Listener
from pathlib import Path
import os
import json
import time
from mss import mss
import hashlib
from datetime import datetime

# accomplishes many things
# - abort the function early if q is held
# - wait inbetween keypresses
# - log a message in the terminal regarding 
#	what key is pressed
def press_key(key: str) -> None:
	if keyboard.is_pressed('q') == True:
		return

	time.sleep(0.15)

	print(f'pressed: {key}')
	keyboard.press_and_release(key)

# frequently used keystrokes
def alt_tab():return press_key('alt+tab')
def ctrl_l(): return press_key('ctrl+l')
def ctrl_a(): return press_key('ctrl+a')
def ctrl_c(): return press_key('ctrl+c')
def ctrl_v(): return press_key('ctrl+v')
def enter():  return press_key('enter')

def write_text(text: str, url=False) -> None:
	if keyboard.is_pressed('q') == True:
		return

	time.sleep(0.2)

	# an easy way to get the url and append the extension
	if url:
		text = f'https://www.humblebundle.com/membership/{text}'

	print(f'wrote: {text}')
	Controller().type(text)

def format_month(url: str) -> str:
	month, year = url.split('-')
	return f'{month.capitalize()} {year}:'

# listens to the mouse until it is clicked
def get_browser_location() -> int, int:
	coords = []
	def on_click(x, y, button, pressed):
		if pressed:
			coords.append(x)
			coords.append(y)
		if not pressed and len(coords) == 2:
			return False
	
	with Listener(on_click=on_click) as listen:
		listen.join()

	x = coords[0] 
	y = coords[1]
	print(f'Clicked at ({x}, {y})')
	
	return x, y

# wait for a change on the screen within a certain region
# used to detect when a webpage updates
def detect_change(x: int, y: int) -> None:
	sct = mss()
	region = {'top': y, 'left': x, 'width': 200, 'height': 200}

	print(f'scanning at ({x}, {y})...')
	previous_hash = None

	while True:
		if keyboard.is_pressed('q') == True:
			return

		img = sct.grab(region)

		current_hash = hashlib.md5(img.rgb).hexdigest()

		if previous_hash and current_hash != previous_hash:
			print(f'change detected!')
			time.sleep(0.5)
			print('proceeding...')
			return

		previous_hash = current_hash
		time.sleep(0.1)

def iterate_url(current_url: str) -> str:
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

if __name__ == '__main__':
	print('make sure you have a browser opened with the appropriate extension installed AND a text editor open')
	print()
	print('do not press any key or click anything other than what is instructed')
	print()
	print('once the keyboard automation begins hold "q" if you need to abort')
	print('Press "ENTER" to continue.')
	
	keyboard.wait('enter')
	time.sleep(0.6)

	# this will be the oldest URL from humble bundle and iterate forward
	root_path = Path(__file__).resolve().parent
	file_path = os.path.join(root_path, 'info.json')

	with open(file_path) as file:
		user_info = json.load(file)

	# trim the url to be just the extension 
	# e.g. current_url = 'december-2019'
	full_url = user_info.get('oldest_url')
	current_url = full_url.split('/')[-1]

	# get the current month and year as a string
	today = datetime.now()
	this_month = f'{today.date():%B}'.lower()
	this_year = f'{today.date():%Y}'
	end_url = f'{this_month}-{this_year}'
	first_loop = True

	print('click on the middle of your browser.')
	x, y = get_browser_location()

	print('now, click into your text editor and press "enter"')
	keyboard.wait('enter')
	time.sleep(0.6)

	# this is to remove the ENTER that the user just input
	press_key('backspace')

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
			# create a new tab
			press_key('ctrl+t')
			first_loop = False
		time.sleep(0.2)
		ctrl_l()
		write_text(current_url, url=True)
		enter()

		# wait for page to load
		detect_change(x, y)	

		# get all games from that page
		ctrl_a()
		time.sleep(0.2)
		ctrl_c()
		alt_tab()

		# document what section the games were taken from
		write_text(format_month(current_url))
		enter()
		# paste games in text editor
		ctrl_v()
		
		if current_url != end_url:
			# change current_url to next page
			current_url = iterate_url(current_url)
		else:
			break

		# for notepad formatting
		enter()
		enter()
		
	print('done.')
