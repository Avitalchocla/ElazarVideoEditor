import os
import subprocess
import stat
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.video import Video
from kivy.utils import platform
from kivy.core.text import LabelBase

# מנגנון הגנה מפני קריסה - טעינת גופן רק אם הוא קיים
font_path = os.path.join(os.path.dirname(__file__), "arial.ttf")
HEBREW = None
if os.path.exists(font_path):
    try:
        LabelBase.register(name="HebrewFont", fn_regular=font_path)
        HEBREW = "HebrewFont"
    except:
        HEBREW = None

class ElazarEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=5, padding=10, **kwargs)
        
        self.ffmpeg_bin = os.path.join(os.path.dirname(__file__), "ffmpeg")
        self.video_path = None
        self.audio_path = None

        # נגן תצוגה מקדימה
        self.preview = Video(source='', state='stop', size_hint_y=0.3)
        self.add_widget(self.preview)

        status_text = "Select Video / בחר סרטון" if HEBREW else "Select Video"
        self.status_label = Label(text=status_text, font_name=HEBREW, size_hint_y=0.05)
        self.add_widget(self.status_label)

        # סייר קבצים
        path = '/sdcard/Download' if platform == 'android' else os.path.expanduser("~")
        self.file_chooser = FileChooserIconView(
            path=path,
            filters=['*.mp4', '*.MP4', '*.mp3', '*.MP3'],
            size_hint_y=0.45
        )
        self.file_chooser.bind(selection=self.on_selection)
        self.add_widget(self.file_chooser)

        # כפתורים
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        txt_v = "SET VIDEO / קבע וידאו" if HEBREW else "SET VIDEO"
        txt_a = "SET AUDIO / קבע אודיו" if HEBREW else "SET AUDIO"
        
        self.btn_v = Button(text=txt_v, font_name=HEBREW, on_release=self.set_video)
        self.btn_a = Button(text=txt_a, font_name=HEBREW, on_release=self.set_audio)
        btn_layout.add_widget(self.btn_v)
        btn_layout.add_widget(self.btn_a)
        self.add_widget(btn_layout)

        # כפתור מיקס
        mix_text = "START MIX / התחל מיקס" if HEBREW else "START MIX"
        self.mix_btn = Button(
            text=mix_text, font_name=HEBREW,
            size_hint_y=0.1, background_color=(0, 0.6, 0, 1),
            on_release=self.run_mix
        )
        self.add_widget(self.mix_btn)

    def on_selection(self, instance, selection):
        if selection:
            path = selection[0]
            if path.lower().endswith(('.mp4', '.MP4')):
                self.preview.source = path
                self.preview.state = 'play'

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = "Video Selected ✅"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = "Audio Selected ✅"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            return

        output_path = "/sdcard/Download/final_mix.mp4"
        if os.path.exists(self.ffmpeg_bin):
            os.chmod(self.ffmpeg_bin, os.stat(self.ffmpeg_bin).st_mode | stat.S_IEXEC)

        cmd = [
            self.ffmpeg_bin, "-y", "-i", self.video_path, "-i", self.audio_path,
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
        ]
        try:
            subprocess.run(cmd, check=True)
            self.status_label.text = "SUCCESS! Saved in Downloads"
        except:
            self.status_label.text = "Error in Mix"

class ElazarEditorApp(App):
    def build(self):
        return ElazarEditor()

if __name__ == '__main__':
    ElazarEditorApp().run()
