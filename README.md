# Program Information

This python script search for **Spotify.exe** instance in process and get the unique title that include artist - song of currently played song and by utilizing **Selenium** with **EdgeWebDriver** to scrape **Bing** for its automatic summary of lyrics and print it out

# Why did I create this?
Spotify silently block free-user from its lyrics and limit them into 2-3 song each day, this absolutely wreck me up as I'm way to irritated to open my browser and search for the lyric manually.

Because of all that I created this little script that I have been using for the past 3 months, and now that Spotify decided that it will maintain the access to lyrics for free-user, this script is no longer needed

# You want to run it?

Get the required python package:

    pip install selenium pywinauto psutil

Get WebDriver for Edge and make sure EdgeWebDriver have the same version with Edge browser [EdgeWebDriver is included in here as per version 127.0.2651.86 (Official build) (64-bit)]

Run the program to catch your Spotify song's lyrics
