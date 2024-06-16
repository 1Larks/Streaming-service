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

class MainScreen(Screen):
    def __init__(self, username, logout_callback, search_callback, play_callback, pause_callback, seek_callback, **kwargs):
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
        self.skip_button = Button(text='>>', size_hint=(None, 1))
        self.rewind_button = Button(text='<<', size_hint=(None, 1))
        self.play_bar.add_widget(self.rewind_button)
        self.play_bar.add_widget(self.play_button)
        self.play_bar.add_widget(self.skip_button)
        self.play_bar.add_widget(self.seek_slider)

        self.song_label = Label(text='Song Name: ')  # Placeholder for song name display

        # Variables to track current playing state
        self.currently_playing = False
        self.current_song_id = None

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
                albums_layout.add_widget(album_button)
            self.content_layout.add_widget(albums_layout)

    def play_song(self, song_id):
        """Play selected song."""
        if self.current_song_id:
            self.stop_song()
            self.pause_callback(stop=True)  # Stop current playback if any
        
        self.play_callback(str(song_id))  # Start playing the new song
        self.currently_playing = True
        self.current_song_id = str(song_id)
        self.layout.add_widget(self.play_bar)  # Show play controls

    def stop_song(self):
        """Stop currently playing song."""
        self.currently_playing = False
        self.current_song_id = None
        self.play_button.text = 'Play'
        self.seek_slider.value = 0

        # Remove play controls
        if self.play_bar in self.layout.children:
            self.layout.remove_widget(self.play_bar)

def popup_message(message, title):
    """Display a popup message."""
    popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
    popup.open()
