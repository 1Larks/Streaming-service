from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

from User_Handler import return_values
from Network_Handler import Network_Handler

Window.size = (400, 600)

class LimitedTextInput(TextInput):
    max_chars = NumericProperty(12)

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_chars:
            substring = substring[:self.max_chars - len(self.text)]
        return super().insert_text(substring, from_undo)

class LoginScreen(BoxLayout):
    def __init__(self, login_callback, register_callback, network_handler,**kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 40
        self.spacing = 20

        self.login_callback = login_callback
        self.register_callback = register_callback

        # Logo
        self.logo = Image(source='logo.png', size_hint=(0.8, None))
        self.add_widget(self.logo)

        # Spacer
        self.add_widget(Widget(size_hint=(1, 0.1)))

        # Username TextInput
        self.username = LimitedTextInput(
            hint_text='Username',
            size_hint=(0.8, None),
            height=40,
            multiline=False,
            max_chars=12
        )
        self.username.halign = 'center'
        self.username.valign = 'middle'
        self.username.bind(minimum_height=self.username.setter('height'))
        self.add_widget(self.username)

        # Password TextInput
        self.password = LimitedTextInput(
            hint_text='Password',
            password=True,
            size_hint=(0.8, None),
            height=40,
            multiline=False,
            max_chars=12
        )
        self.password.halign = 'center'
        self.password.valign = 'middle'
        self.password.bind(minimum_height=self.password.setter('height'))
        self.add_widget(self.password)

        # Login Button
        self.login_button = Button(
            text='Login',
            size_hint=(0.8, None),
            height=40,
            background_color=(0, 0.5, 1, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            bold=True
        )
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)

        # Register Button
        self.register_button = Button(
            text='Register',
            size_hint=(0.8, None),
            height=40,
            background_color=(0, 0.5, 1, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            bold=True
        )
        self.register_button.bind(on_press=self.register)
        self.add_widget(self.register_button)
        
        self.network_h = network_handler

    def login(self, instance):
        username = self.username.text
        password = self.password.text
        self.login_callback(username, password)
        result = self.network_h.getAsyncBuffer('auth')
        if result == 'S':
            self.add_widget(Label(text=f'[color=FF0000]{result}[/color]', markup=True, size_hint=(0.8, None)))
        else:
            self.add_widget(Label(text=f'[color=FF0000]{result}[/color]', markup=True, size_hint=(0.8, None)))

    def register(self, instance):
        username = self.username.text
        password = self.password.text
        self.register_callback(username, password)
        result = self.network_h.getAsyncBuffer('auth')
        if result == return_values['S']:
            self.add_widget(Label(text=f'[color=FF0000]{result}[/color]', markup=True, size_hint=(0.8, None)))
        else:
            self.add_widget(Label(text=f'[color=FF0000]{return_values[result]}[/color]', markup=True, size_hint=(0.8, None)))

class LoginApp(App):
    def __init__(self, login_callback, register_callback, network_handler, **kwargs):
        super(LoginApp, self).__init__(**kwargs)
        self.login_callback = login_callback
        self.register_callback = register_callback
        self.network_h = network_handler
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        login_screen = LoginScreen(self.login_callback, self.register_callback, self.network_h)
        layout.add_widget(login_screen)
        return layout
