import psutil
from pywinauto import Desktop # type: ignore

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This method works but it kinda slow because need the check every process
def get_spotify_song_info_by_process_search():
    # spotify executable names
    spotify_executables = ["Spotify.exe", "Spotify"]
    # get all windows on the desktop
    windows = Desktop(backend="uia").windows()
    for win in windows:
        title = win.window_text()
        if " - " in title and len(title.split(" - ")) == 2:
            pid = win.process_id()
            try:
                process = psutil.Process(pid)
                process_name = process.name()
                if process_name in spotify_executables:
                    artist, song = title.split(" - ", 1)
                    return artist.strip(), song.strip()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    return None, None

# This method works way faster and accurate since you could set the Spotify's PID (task manager -> details) but the PID is keep changing for each application start-up
def get_spotify_song_info_by_pid(pid):
    try:
        process = psutil.Process(pid)
        if process.name() in ["Spotify.exe", "Spotify"]:
            windows = Desktop(backend="uia").windows(process=pid)
            for win in windows:
                title = win.window_text()
                if " - " in title and len(title.split(" - ")) == 2:
                    artist, song = title.split(" - ", 1)
                    return artist.strip(), song.strip()
        else:
            return None, None
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None, None

def get_spotify_title():
    spotify_pid = 11344  # Spotify's PID, where the title song shown in task manager
    artist, song = get_spotify_song_info_by_process_search()
    #artist, song = get_spotify_song_info_by_pid(spotify_pid)
    if artist and song:
        print(f"Currently playing: {song} by {artist}")
        return(f"{artist} {song}")
    else:
        print("Spotify process not found or no song playing")

def bing_auto_summary_lyrics_catcher(path, search):
    # path to webdriver
    edge_driver_path = path

    # settings
    edge_options = Options()
    edge_options.use_chromium = True  # using chromium-based
    # no_gui_mode
    edge_options.add_argument('--headless')
    edge_options.add_argument('--disable-gpu')

    # webdriver services startup
    service = Service(executable_path=edge_driver_path)

    # supress warning? didn't work (related to no_gui_mode)
    #sys.stderr = open(os.devnull, 'w')

    # initalized the webdriver services and options
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        # search the web
        driver.get(f'https://www.bing.com/search?q={search}')
        
        # wait for javascript to load from the webpage
        lyrics_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/ol/li[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[1]'))
        )
        
        # get child div of class "lyrics" that is "verse tc_translated"
        verse_divs = lyrics_div.find_elements(By.CLASS_NAME, 'verse')
        
        #lyrics = "\n".join(div.text for div in verse_divs)
        lyrics = []
        for div in verse_divs:
            inner_html = div.get_attribute('innerHTML')
            # take <br> with new line for printing
            formatted_text = inner_html.replace('<br>', '\n').replace('<p>', '\n\n').replace('</p>', '')
            lyrics.append(formatted_text.strip())

        lyrics_output = '\n\n'.join(lyrics).strip()
        print("Lyric found: \n")
        print(lyrics_output +" \n")
        
    except Exception as e:
        #print("Exception:", e)
        #print("Page source at error:", driver.page_source)
        #print("Current URL:", driver.current_url)
        print("Cannot find the lyric (No summary from Bing) or Timeout has occured")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    song_info = get_spotify_title()
    if song_info:
        bing_auto_summary_lyrics_catcher('msedgedriver.exe', song_info + ' lyrics')