from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

class myApp(MDApp):
    def build(self):
        label = MDLabel(text="Hello Hassan", halign="center", theme_text_color="Secondary")
        return label

myApp().run()
