import os
import subprocess
import stat
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.utils import platform

class VideoAudioMixer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)
        
        self.ffmpeg_bin = os.path.join(os.path.dirname(__file__), "ffmpeg")
        self.video_path = None
        self.audio_path = None
        
        self.add_widget(Label(text="ELAZAR EDITOR V4.0", font_size='24sp', size_hint_y=0.1))
        
        # סייר קבצים פשוט
        # אם הוא לא מראה קבצים, נסה ללחוץ על התיקיות עד שתגיע ל-Download
        path = '/sdcard' if platform == 'android' else os.path.expanduser("~")
        self.file_chooser = FileChooserIconView(path=path, filters=['*.mp4', '*.MP4', '*.mp3', '*.MP3'])
        self.add_widget(self.file_chooser)
        
        self.status_label = Label(text="Status: Ready", size_hint_y=0.1)
        self.add_widget(self.status_label)
        
        btns = BoxLayout(size_hint_y=0.2, spacing=10)
        btns.add_widget(Button(text="SELECT VIDEO", on_release=self.set_video))
        btns.add_widget(Button(text="SELECT AUDIO", on_release=self.set_audio))
        btns.add_widget(Button(text="START MIX", background_color=(0, 0.7, 0, 1), on_release=self.run_mix))
        self.add_widget(btns)

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = "Video Selected"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = "Audio Selected"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "Select files first!"
            return

        output_path = "/sdcard/Download/final_mix.mp4"

        # הרשאת הרצה ל-ffmpeg
        if os.path.exists(self.ffmpeg_bin):
            os.chmod(self.ffmpeg_bin, os.stat(self.ffmpeg_bin).st_mode | stat.S_IEXEC)

        cmd = [
            self.ffmpeg_bin, "-y", "-i", self.video_path, "-i", self.audio_path,
            "-c:v", "copy", "-c:a", "aac", "-shortest", output_path
        ]

        try:
            self.status_label.text = "Mixing..."
            subprocess.run(cmd, check=True)
            self.status_label.text = "Success! Saved in Downloads"
        except:
            self.status_label.text = "Mix Failed"

class ElazarEditorApp(App):
    def build(self):
        # בקשת הרשאות בסיסיות בלבד בסטארט-אפ
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        return VideoAudioMixer()

if __name__ == '__main__':
    ElazarEditorApp().run()
