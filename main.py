from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import os

# ממשק המשתמש (UI) מוטמע ישירות למניעת קריסות פתיחה
kv_string = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    canvas.before:
        Color:
            rgba: (0.1, 0.1, 0.15, 1)
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "ELAZAR VIDEO EDITOR"
        font_size: '26sp'
        bold: True
        size_hint_y: 0.15
        color: (1, 0.6, 0, 1)

    BoxLayout:
        orientation: 'vertical'
        spacing: 5
        size_hint_y: 0.2
        Label:
            text: "Video File:"
            halign: 'left'
            text_size: self.size
        BoxLayout:
            spacing: 10
            TextInput:
                id: vid_input
                hint_text: "Select video..."
                multiline: False
            Button:
                text: "Browse"
                size_hint_x: 0.3
                on_press: app.open_file_manager('video')

    BoxLayout:
        orientation: 'vertical'
        spacing: 5
        size_hint_y: 0.2
        Label:
            text: "Audio File (MP3):"
            halign: 'left'
            text_size: self.size
        BoxLayout:
            spacing: 10
            TextInput:
                id: aud_input
                hint_text: "Select audio..."
                multiline: False
            Button:
                text: "Browse"
                size_hint_x: 0.3
                on_press: app.open_file_manager('audio')

    Label:
        id: status
        text: "Ready"
        size_hint_y: 0.1
        color: (0.7, 0.7, 0.7, 1)

    Button:
        text: "MIX VIDEO & AUDIO"
        size_hint_y: 0.2
        bold: True
        background_normal: ''
        background_color: (1, 0.4, 0, 1)
        on_press: app.start_processing()
'''

class VideoEditorApp(App):
    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])
        return Builder.load_string(kv_string)

    def open_file_manager(self, target):
        content = FileChooserIconView(path='/storage/emulated/0/')
        popup = Popup(title="Select File", content=content, size_hint=(0.9, 0.9))
        
        def on_selection(instance, selection):
            if selection:
                if target == 'video':
                    self.root.ids.vid_input.text = selection[0]
                else:
                    self.root.ids.aud_input.text = selection[0]
                popup.dismiss()

        content.bind(on_submit=on_selection)
        popup.open()

    def start_processing(self):
        v = self.root.ids.vid_input.text
        a = self.root.ids.aud_input.text
        if not v or not a:
            self.root.ids.status.text = "❌ Please select both files"
            return
        
        self.root.ids.status.text = "🔄 Processing... (This takes a moment)"
        # כאן יבוצע החיבור בעזרת ffmpeg-kit בשלב הבא

if __name__ == "__main__":
    VideoEditorApp().run()
