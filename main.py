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

# 1. טעינת גופן עברי (חובה שהקובץ יהיה בתיקייה!)
font_path = "arial.ttf"
if os.path.exists(font_path):
    LabelBase.register(name="HebrewFont", fn_regular=font_path)
    HEBREW = "HebrewFont"
else:
    HEBREW = None # ברירת מחדל אם אין קובץ

class ElazarEditor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=5, padding=10, **kwargs)
        
        self.ffmpeg_bin = os.path.join(os.path.dirname(__file__), "ffmpeg")
        self.video_path = None
        self.audio_path = None

        # נגן תצוגה מקדימה
        self.preview = Video(source='', state='stop', size_hint_y=0.3)
        self.add_widget(self.preview)

        self.status_label = Label(text="בחר סרטון כדי לצפות בו", font_name=HEBREW, size_hint_y=0.05)
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

        # כפתורים בעברית
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        self.btn_v = Button(text="קבע כסרטון", font_name=HEBREW, on_release=self.set_video)
        self.btn_a = Button(text="קבע כאודיו", font_name=HEBREW, on_release=self.set_audio)
        btn_layout.add_widget(self.btn_v)
        btn_layout.add_widget(self.btn_a)
        self.add_widget(btn_layout)

        # כפתור ביצוע
        self.mix_btn = Button(
            text="התחל מיקס", 
            font_name=HEBREW,
            size_hint_y=0.1, 
            background_color=(0, 0.6, 0, 1),
            on_release=self.run_mix
        )
        self.add_widget(self.mix_btn)

    def on_selection(self, instance, selection):
        if selection:
            path = selection[0]
            if path.lower().endswith(('.mp4', '.MP4')):
                self.preview.source = path
                self.preview.state = 'play'
                self.status_label.text = "מציג סרטון..."

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.btn_v.text = "וידאו נבחר ✅"
            self.status_label.text = "עכשיו בחר קובץ אודיו"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.btn_a.text = "אודיו נבחר ✅"
            self.status_label.text = "מוכן למיקס!"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "חובה לבחור את שני הקבצים!"
            return

        output_path = "/sdcard/Download/final_mix.mp4"
        if os.path.exists(self.ffmpeg_bin):
            os.chmod(self.ffmpeg_bin, os.stat(self.ffmpeg_bin).st_mode | stat.S_IEXEC)

        cmd = [
            self.ffmpeg_bin, "-y", "-i", self.video_path, "-i", self.audio_path,
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
        ]

        try:
            self.status_label.text = "מבצע מיקס... נא להמתין"
            subprocess.run(cmd, check=True)
            self.status_label.text = "הצלחה! הקובץ נשמר בהורדות"
        except:
            self.status_label.text = "שגיאה בביצוע המיקס"

class ElazarEditorApp(App):
    def build(self):
        return ElazarEditor()

if __name__ == '__main__':
    ElazarEditorApp().run()
