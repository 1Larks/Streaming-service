from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.clock import Clock

class MainScreen(Screen):
    def __init__(self, username, logout_callback, search_callback, play_callback, pause_callback,
                 seek_callback, get_song_info_callback, get_neighboring_songs_callback, 
                 has_ended, get_album_song, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Background color setup
        with self.canvas.before:
            Color(0.19607843137, 0.19607843137, 0.19607843137, 1)  # Dark gray color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.name = 'main_screen'
        self.username = username
        self.logout_callback = logout_callback
        self.search_callback = search_callback
        self.play_callback = play_callback
        self.pause_callback = pause_callback
        self.seek_callback = seek_callback
        self.get_song_info_callback = get_song_info_callback
        self.get_neighboring_songs_callback = get_neighboring_songs_callback
        self.has_ended = has_ended
        self.get_album_song = get_album_song
        
        # Main layout setup
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.layout)

        # Top bar layout
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.layout.add_widget(top_bar)

        # Search bar and button
        search_layout = BoxLayout(orientation='horizontal', size_hint_x=0.8)
        self.search_input = TextInput(hint_text='Search', size_hint_y=0.9, height=30, multiline=False)
        search_button = Button(text='Search', size_hint_y=0.9, height=30, size_hint_x=0.3)
        search_button.bind(on_press=self.search_for_song)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        search_layout.add_widget(Widget(size_hint=(0.4, None)))  # Spacer
        top_bar.add_widget(search_layout)

        # Username button and dropdown menu
        user_layout = BoxLayout(orientation='horizontal', size_hint_x=0.2)
        user_button = Button(text=self.username, size_hint_y=None, height=30)
        dropdown = DropDown()
        logout_btn = Button(text='Log out', size_hint_y=None, height=30)
        logout_btn.bind(on_release=lambda x: self.logout_callback())
        dropdown.add_widget(logout_btn)
        user_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(user_button, 'text', x))
        user_layout.add_widget(user_button)
        top_bar.add_widget(user_layout)

        # Content layout
        self.content_layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.content_layout)

        # Play controls layout (initially hidden)
        self.play_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.play_button = Button(text='Pause', size_hint=(None, 1))
        self.play_button.bind(on_press=self.toggle_play)
        self.seek_slider = Slider(min=0, max=100, value=0)
        self.seek_slider.bind(on_touch_up=self.on_slider_touch_up)
        self.time_label = Label(text='00:00')
        self.skip_button = Button(text='>>', size_hint=(None, 1))
        self.skip_button.bind(on_press=lambda x: self.skip())
        self.rewind_button = Button(text='<<', size_hint=(None, 1))
        self.rewind_button.bind(on_press=lambda x:self.rewind())
        self.play_bar.add_widget(self.rewind_button)
        self.play_bar.add_widget(self.play_button)
        self.play_bar.add_widget(self.skip_button)
        self.play_bar.add_widget(self.seek_slider)
        self.play_bar.add_widget(self.time_label)
        
        self.song_label = Label(text='Song Name: ')  # Placeholder for song name display
        
        self.next = None
        self.prev = None
        self.elapsed_seconds = 0
        
        # Variables to track current playing state
        self.currently_playing = False
        self.current_song_id = None
        Clock.schedule_interval(self.update_slider, 1)

    def rewind(self):
        if self.elapsed_seconds > 3:
            self.play_song(self.current_song_id)
        else:
            self.play_song(self.prev)
        
        
    def skip(self):
        self.play_song(self.next)

    def toggle_play(self, instance):
        """Toggle play/pause state."""
        if self.play_button.text == 'Play':
            self.play_button.text = 'Pause'
            self.play_callback(self.current_song_id)  # Call play function
        else:
            self.play_button.text = 'Play'
            self.pause_callback()  # Call pause function

    def on_slider_touch_up(self, instance, touch):
        """Handle slider touch event."""
        if instance.collide_point(*touch.pos) and touch.grab_current == instance:
            self.pause_callback()
            value = instance.value / 100
            self.seek_callback(value)
            if self.play_button.text == 'Pause':
                self.play_callback(self.current_song_id)
            touch.ungrab(instance)
    
    def update_slider(self, dt):
        if self.currently_playing and self.current_song_id:
            info = self.get_song_info_callback()
            current_frame = info[0]
            total_frames = info[1]
            sample_rate = info[2]
            frame_size = info[3]
            if not self.has_ended():
                if total_frames > 0:
                    self.seek_slider.value = (current_frame / (total_frames)) * 100 
                self.elapsed_seconds = (current_frame/frame_size) / sample_rate
                minutes = int(self.elapsed_seconds // 60)
                seconds = int(self.elapsed_seconds % 60)
                self.time_label.text = f'{minutes:02}:{seconds:02}'
            else:
                self.skip()
            
                
    
    def search_for_song(self, instance):
        """Handle search button press."""
        search_query = self.search_input.text.strip()
        if search_query and len(search_query) < 12:
            result = self.search_callback(search_query)
            self.display_results(result)

    def _update_rect(self, instance, value):
        """Update background"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def display_results(self, results):
        """Display search results."""
        self.content_layout.clear_widgets()

        if 'songs' in results:
            songs_layout = BoxLayout(orientation='horizontal', height=100)
            self.content_layout.add_widget(Label(text='Songs:', size_hint_y=None, height=30))
            for item in results['songs']:
                song_button = Button(text=item[2], size_hint_x=None, width=200, height=150)
                song_button.bind(on_release=lambda instance, song_id=item[1]: self.play_song(song_id))
                songs_layout.add_widget(song_button)
            self.content_layout.add_widget(songs_layout)

        if 'albums' in results:
            albums_layout = BoxLayout(orientation='horizontal', height=100)
            self.content_layout.add_widget(Label(text='Albums:', size_hint_y=None, height=30))
            for item in results['albums']:
                album_button = Button(text=item[2], size_hint_x=None, width=200, height=150)
                album_button.bind(on_release=lambda instance, album_id=item[1]: self.play_album(album_id))
                albums_layout.add_widget(album_button)
            self.content_layout.add_widget(albums_layout)

    def play_song(self, song_id):
        """Play selected song."""
        if self.current_song_id:
            self.stop_song()
            self.pause_callback(stop=True)  # Stop current playback if any
            if self.play_bar in self.layout.children:
                self.layout.remove_widget(self.play_bar)
        self.next = self.get_neighboring_songs_callback('NEXT', str(song_id))
        self.prev = self.get_neighboring_songs_callback('PREV', str(song_id))
        
        self.play_callback(str(song_id))  # Start playing the new song
        self.play_button.text = 'Pause'
        self.currently_playing = True
        self.current_song_id = str(song_id)
        self.layout.add_widget(self.play_bar)  # Show play controls
    
    def play_album(self, album_id):
        song_id = self.get_album_song(album_id)
        self.play_song(song_id) 
    
    def stop_song(self):
        """Stop currently playing song."""
        self.currently_playing = False
        self.current_song_id = None
        self.seek_slider.value = 0
        
def popup_message(message, title):
    """Display a popup message."""
    popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
    popup.open()
