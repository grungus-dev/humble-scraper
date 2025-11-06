# Welcome to the Humble Bundle Membership Webscraper
I'm going to start out by saying that this whole process is a lot more janky than I originally intended it to be. But this is the solution I ended up coming to so just read what I got to say.

This webscraping process relies on a few things:
- A Chromium based browser
	- A custom extension to be installed on this browser
- A basic text editor
- Admin permissions
	- This is due to the Python script using your keyboard... a lot

# Installing the extension
this script relies on a custom chrome extension to be installed in your browser beforehand.

Your browser needs to be Chrome, Brave, or any Chromium based browser that supports extensions.

In your browser you are going to navigate to wherever you manage extensions.  After that you are going to toggle Developer mode to ON.

Once you are in Developer mode you should see a button to load an unpacked extension. Click on it and route it to the Extension folder wherever you cloned this repository.

This extension only affects the Humble Bundle membership page and is active automatically. So whenever you aren't using this script I recommend you turn it off.

# setting up the script
This script uses a file called "info.json" to get the oldest month of membership on your humble bundle account. For the guy I'm making this for this is already set to his oldest URL so he doesn't have to worry about it.

You also need to have your browser on your main monitor. It doesn't matter where your terminal and text editor are, but the browser needs to be on your main monitor, ideally fullscreened.

This may be obvious but you also need to be logged into your Humble Bundle account for this process to work.

# putting it all together
To initialize the script, make sure you run the script using admin privileges. On Linux this would mean making sure you use "sudo" before running the script.

Once the script is running it is going to ask you if you have everything you need running, press enter once you have everything pulled up.

It will then ask you to click on the center of your browser. This is to calibrate where it will be looking for changes in the webpage. Make sure you dont click near the address bar as that can add some unintended behavior.

Lastly it will ask you to click into your notepad and hit enter. This will set off the process and it should do everything from there.

I've done a lot of testing and it is pretty consistent currently, but sometimes there can be some kind of desync with the browser detection. If something ever happens and you need to close the program hold "q" and it will stop as early as it can.

Other than that, sit back and watch your membership games get documented for you.
