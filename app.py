import time
import json
import asyncio  
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

    async def login(self, user, passwd):
        self.browser.get(LOGIN_URL + self.playlist)
        await asyncio.sleep(2)

        # Find and input user and password
        username = self.browser.find_element_by_name("username")
        username.send_keys(user)

        password = self.browser.find_element_by_name("password")
        password.send_keys(passwd)
        
        # Login
        button  = self.browser.find_element_by_id('login-button')
        button.click()
        
        await asyncio.sleep(2)

    def quit(self):
        self.browser.quit()
    
    async def play(self, wait):
        header = self.browser.find_elements_by_css_selector('div.TrackListHeader__button')[0]
        play = header.find_elements_by_css_selector('button.btn-green')
        play[0].click()

        self.browser.save_screenshot('debug.png')
        await asyncio.sleep(wait)
        self.browser.quit()

async def run(account, config):            
    print('Load: ' + account['username'])
    spotify = Spotify(config['playlist'])

    await spotify.login(account['username'], account['password'])
    await spotify.play(config['wait'])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    config = json.loads(open('config.json', 'r').read())
    print('Playlist: ' + config['playlist'])
    
    while True:
        tasks = []
        for account in config['accounts']:
            tasks.append(asyncio.ensure_future(run(account, config))),
        loop.run_until_complete(asyncio.wait(tasks))
        
    loop.close()
