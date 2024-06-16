from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

class LimitedTextInput(TextInput):
    """
    A custom made TextInput Widget for the project's needs
    """
    max_chars = NumericProperty(12)

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_chars:
            substring = substring[:self.max_chars - len(self.text)]
        return super().insert_text(substring, from_undo=from_undo)

class LoginScreen(Screen):
    def __init__(self, login_callback, register_callback, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.name = 'login_screen'
        
        #Change background color
        with self.canvas.before:
            Color(0.19607843137, 0.19607843137, 0.19607843137, 1)  # Dark gray color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Callback functions
        self.login_callback = login_callback
        self.register_callback = register_callback
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.add_widget(self.layout)

        # Logo
        self.logo = Image(source='logo.png', pos_hint={'center_x': 0.5})
        self.layout.add_widget(self.logo)

        # Spacer
        self.layout.add_widget(Widget(size_hint_y=None, height=20))

        # Username TextInput
        self.username = LimitedTextInput(
            hint_text='Username',
            size_hint=(0.5, None),
            pos_hint={'center_x': 0.5},
            height=40,
            multiline=False,
            max_chars=12
        )
        self.username.halign = 'center'
        self.username.valign = 'middle'
        self.username.bind(minimum_height=self.username.setter('height'))
        self.layout.add_widget(self.username)

        # Password TextInput
        self.password = LimitedTextInput(
            hint_text='Password',
            password=True,
            size_hint=(0.5, None),
            pos_hint={'center_x': 0.5},
            height=40,
            multiline=False,
            max_chars=12
        )
        self.password.halign = 'center'
        self.password.valign = 'middle'
        self.password.bind(minimum_height=self.password.setter('height'))
        self.layout.add_widget(self.password)

        # Login Button
        self.login_button = Button(
            text='Login',
            size_hint=(0.5, None),
            pos_hint={'center_x': 0.5},
            height=40,
            background_color=(0, 0.5, 1, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            bold=True
        )
        self.login_button.bind(on_press=self.login)
        self.layout.add_widget(self.login_button)

        # Register Button
        self.register_button = Button(
            text='Register',
            size_hint=(0.5, None),
            pos_hint={'center_x': 0.5},
            height=40,
            background_color=(0, 0.5, 1, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            bold=True
        )
        self.register_button.bind(on_press=self.register)
        self.layout.add_widget(self.register_button)
        
    def _update_rect(self, instance, value):
        """
        Change background color.
        """
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def login(self, instance):
        """
        Call the callback function if there is available information in the designated text boxes
        """
        username = self.username.text.strip()
        password = self.password.text
        if username and password:
            self.login_callback(username, password)
        
    def register(self, instance):
        """
        Call the callback function if there is available information in the designated text boxes
        """
        username = self.username.text.strip()
        password = self.password.text
        if username and password:
            self.register_callback(username, password)