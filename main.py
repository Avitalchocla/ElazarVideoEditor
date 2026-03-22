import os
import subprocess
import stat
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.utils import platform

# בקשת הרשאות מיוחדת לאנדרואיד
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.MANAGE_EXTERNAL_STORAGE
    ])

class VideoAudioMixer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)
        
        # איתור ה-FFmpeg
        self.ffmpeg_bin = os.path.join(os.path.dirname(__file__), "ffmpeg")
        
        if os.path.exists(self.ffmpeg_bin):
            try:
                st = os.stat(self.ffmpeg_bin)
                os.chmod(self.ffmpeg_bin, st.st_mode | stat.S_IEXEC)
            except:
                pass

        self.video_path = None
        self.audio_path = None
        
        # כותרת באנגלית כדי למנוע ג'יבריש
        self.label = Label(text="ELAZAR EDITOR PRO V3.6", font_size='24sp', size_hint_y=0.1)
        self.add_widget(self.label)
        
        self.status_label = Label(text="Status: Ready", size_hint_y=0.1)
        self.add_widget(self.status_label)
        
        # סייר קבצים
        default_path = '/sdcard' if platform == 'android' else os.path.expanduser("~")
        self.file_chooser = FileChooserIconView(path=default_path, filters=['*.mp4', '*.mp3', '*.m4a', '*.wav'])
        self.add_widget(self.file_chooser)
        
        # כפתורים באנגלית
        btns = BoxLayout(size_hint_y=0.2, spacing=10)
        self.btn_video = Button(text="1. SELECT VIDEO", on_release=self.set_video)
        self.btn_audio = Button(text="2. SELECT AUDIO", on_release=self.set_audio)
        self.btn_mix = Button(text="3. START MIX", background_color=(0, 0.7, 0, 1), on_release=self.run_mix)
        
        btns.add_widget(self.btn_video)
        btns.add_widget(self.btn_audio)
        btns.add_widget(self.btn_mix)
        self.add_widget(btns)

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = f"Video Selected: {os.path.basename(self.video_path)}"
        else:
            self.status_label.text = "Error: No file selected!"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = f"Audio Selected: {os.path.basename(self.audio_path)}"
        else:
            self.status_label.text = "Error: No file selected!"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "MUST SELECT BOTH FILES!"
            return

        # נתיב שמירה בתיקיית הורדות
        output_dir = "/sdcard/Download/ELAZAR_EDITOR"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        output_path = os.path.join(output_dir, "final_mix.mp4")

        self.status_label.text = "Mixing... Please wait"

        # פקודת ה-FFmpeg
        cmd = [
            self.ffmpeg_bin, "-y",
            "-i", self.video_path,
            "-i", self.audio_path,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", output_path
        ]

        try:
            subprocess.run(cmd, check=True)
            self.status_label.text = "SUCCESS! File saved in Download/ELAZAR_EDITOR"
        except Exception as e:
            self.status_label.text = f"Error: FFmpeg failed"

class ElazarEditorApp(App):
    def build(self):
        return VideoAudioMixer()

if __name__ == '__main__':
    ElazarEditorApp().run()
