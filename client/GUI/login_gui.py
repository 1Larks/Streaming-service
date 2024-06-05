from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class LimitedTextInput(TextInput):
    def __init__(self, max_chars, **kwargs):
        super().__init__(**kwargs)
        self.max_chars = max_chars

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_chars:
            substring = substring[:self.max_chars - len(self.text)]
        return super().insert_text(substring, from_undo)

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Logo
        self.logo = Image(source='logo.png')
        self.add_widget(self.logo)

        # Username TextInput
        self.username = LimitedTextInput(
            hint_text='Username',
            max_chars=12,
            size_hint=(1, 0.1)
        )
        self.add_widget(self.username)

        # Password TextInput
        self.password = LimitedTextInput(
            hint_text='Password',
            password=True,
            max_chars=12,
            size_hint=(1, 0.1)
        )
        self.add_widget(self.password)

        # Login Button
        self.login_button = Button(
            text='Login',
            size_hint=(1, 0.1)
        )
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)

        # Register Button
        self.register_button = Button(
            text='Register',
            size_hint=(1, 0.1)
        )
        self.register_button.bind(on_press=self.register)
        self.add_widget(self.register_button)

    def login(self, instance):
        username = self.username.text
        password = self.password.text
        self.parent.login_callback(username, password)

    def register(self, instance):
        username = self.username.text
        password = self.password.text
        self.parent.register_callback(username, password)

class LoginApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_callback = None
        self.register_callback = None

    def build(self):
        root = BoxLayout(orientation='vertical')
        self.login_screen = LoginScreen()
        root.add_widget(self.login_screen)
        return root

    def set_callbacks(self, login_callback, register_callback):
        self.login_screen.parent = self
        self.login_callback = login_callback
        self.register_callback = register_callback

if __name__ == '__main__':
    app = LoginApp()
    app.run()