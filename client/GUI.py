from User_Handler import return_values
from login_gui import LoginScreen
from main_screen import MainScreen, popup_message
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

class AudioStreamingApp(App):
    def __init__(self, network_h, user_h, stream_h, **kwargs):
        super(AudioStreamingApp, self).__init__(**kwargs)
        self.network_h = network_h
        self.user_h = user_h
        self.stream_h = stream_h
        self.screen_manager = ScreenManager()

    def build(self):
        self.login_screen = LoginScreen(self.login_callback, self.register_callback)
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.current = 'login_screen'
        
        return self.screen_manager
    
    def build_main_screen(self):
        self.main_screen = MainScreen(self.user_h.username, self.logout_callback, self.search_callback, self.play_callback, self.pause_callback, self.seek_callback)
        self.screen_manager.add_widget(self.main_screen)
    
    def login_callback(self, username, password):
        self.user_h.login(username, password)
        response = self.network_h.getAsyncBuffer('auth')
        if return_values[response] == return_values['S'] and len(username)>0:
            self.build_main_screen()
            self.screen_manager.current = 'main_screen'
        else:
            popup_message(f"Login failed: {return_values[response]}", 'Error')

    def register_callback(self, username, password):
        self.user_h.register_user(username, password)
        response = self.network_h.getAsyncBuffer('auth')
        if return_values[response] == return_values['S'] and len(username)>0:
            self.build_main_screen()
            self.screen_manager.current = 'main_screen'
        else:
            popup_message(f"Registration failed: {return_values[response]}", 'Error')
    def logout_callback(self):
        self.screen_manager.current = 'login_screen'
        self.screen_manager.remove_widget(self.main_screen)
        self.user_h.username = None
        
    def search_callback(self, term):
        self.network_h.send_data('SRCH'+term, text=True)
        res = self.network_h.getAsyncBuffer('search')
        return res
    def play_callback(self, song_id):
        self.network_h.send_data('PLAY'+f'{song_id}:{self.stream_h.frames_received}', text=True)
    
    def pause_callback(self, stop=False):
        self.stream_h.stop_stream()
        self.network_h.send_data('PAUS', text=True)
        if stop:
            self.stream_h.reset_stream()
        
    def seek_callback(self, point):
        point = int(point*self.stream_h.size)
        self.stream_h.frames_received = point