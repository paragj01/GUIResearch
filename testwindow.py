from kivy.app import App
from kivy.uix.widget import Widget
class TestWidget(Widget):
    pass
class TestApp(App):
    def build(self):
        return TestWidget()

if __name__ == '__main__':
    TestApp().run()
