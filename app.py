import time
import json
from selenium import webdriver

LOGIN_URL = "https://accounts.spotify.com/fr/login?continue=https:%2F%2Fopen.spotify.com%2Fplaylist%2F"

class Spotify(object):
    
    def __init__(self, playlist):
        self.playlist = playlist
        
        options = webdriver.ChromeOptions()
        
        # Not work with headless :(
        # options.add_argument("--headless")
        
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.plugins": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
            "PluginsAllowedForUrls": "*.spotify.com"
        })
        self.browser = webdriver.Chrome(options=options)

    def login(self, user, passwd):
        self.browser.get(LOGIN_URL + self.playlist)
        time.sleep(2)

        # Find and input user and password
        username = self.browser.find_element_by_name("username")
        username.send_keys(user)

        password = self.browser.find_element_by_name("password")
        password.send_keys(passwd)
        
        # Login
        button  = self.browser.find_element_by_id('login-button')
        button.click()
        
        time.sleep(2)
        self.play()

    def logout(self):
        self.browser.quit()
    
    def play(self):
        header = self.browser.find_elements_by_css_selector('div.TrackListHeader__button')[0]
        play = header.find_elements_by_css_selector('button.btn-green')
        play[0].click()

        time.sleep(15)
        self.browser.save_screenshot('debug.png')
    
if __name__ == "__main__":
    config = json.loads(open('config.json', 'r').read())
    print('Playlist: ' + config['playlist'])
    
    for account in config['accounts']:
        print('Load: ' + account['username'])
        spotify = Spotify(config['playlist'])

        spotify.login(account['username'], account['password'])
        spotify.play()
