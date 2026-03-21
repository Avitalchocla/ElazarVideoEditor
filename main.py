from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import os
import subprocess

kv_string = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    canvas.before:
        Color:
            rgba: (0.1, 0.1, 0.1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "ELAZAR VIDEO EDITOR"
        font_size: '24sp'
        color: (1, 0.6, 0, 1)

    Button:
        text: "1. SELECT VIDEO"
        size_hint_y: 0.15
        on_press: app.open_file_manager('video')

    Button:
        text: "2. SELECT AUDIO (MP3)"
        size_hint_y: 0.15
        on_press: app.open_file_manager('audio')

    Label:
        id: status
        text: "Select files to begin"
        size_hint_y: 0.1

    Button:
        text: "MIX AND SAVE"
        size_hint_y: 0.2
        bold: True
        background_color: (0, 0.7, 0.3, 1)
        on_press: app.process()
'''

class VideoEditorApp(App):
    video = ""
    audio = ""

    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.MANAGE_EXTERNAL_STORAGE])
        return Builder.load_string(kv_string)

    def open_file_manager(self, target):
        path = '/storage/emulated/0/' if platform == 'android' else os.path.expanduser("~")
        chooser = FileChooserIconView(path=path)
        popup = Popup(title="Select File", content=chooser, size_hint=(0.9, 0.9))

        def on_selection(instance, selection):
            if selection:
                if target == 'video':
                    self.video = selection[0]
                    self.root.ids.status.text = "Video Selected ✅"
                else:
                    self.audio = selection[0]
                    self.root.ids.status.text = "Audio Selected ✅"
                popup.dismiss()

        chooser.bind(on_submit=on_selection)
        popup.open()

    def process(self):
        if not self.video or not self.audio:
            self.root.ids.status.text = "❌ Missing files!"
            return
        
        output = "/storage/emulated/0/Download/ELAZAR_MIXED.mp4"
        
        # אנחנו מנסים להריץ את ה-ffmpeg שהתקנו דרך ה-requirements
        cmd = ["ffmpeg", "-y", "-i", self.video, "-i", self.audio, "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output]
        
        try:
            self.root.ids.status.text = "🔄 Working... please wait"
            subprocess.run(cmd, check=True)
            self.root.ids.status.text = "✅ SUCCESS! Saved to Downloads"
        except Exception as e:
            self.root.ids.status.text = f"❌ Error: {str(e)}"

if __name__ == "__main__":
    VideoEditorApp().run()
