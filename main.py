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
        
        self.add_widget(Label(text="ELAZAR EDITOR V4.2", font_size='24sp', size_hint_y=0.1))
        
        # סייר קבצים שמתחיל בתיקייה הראשית
        path = '/sdcard' if platform == 'android' else os.path.expanduser("~")
        self.file_chooser = FileChooserIconView(
            path=path,
            filters=['*.mp4', '*.MP4', '*.mp3', '*.MP3', '*.m4a', '*.M4A']
        )
        self.add_widget(self.file_chooser)
        
        self.status_label = Label(text="If empty, grant 'All Files Access' in settings", size_hint_y=0.1)
        self.add_widget(self.status_label)
        
        btns = BoxLayout(size_hint_y=0.2, spacing=10)
        btns.add_widget(Button(text="UP (..)", on_release=self.go_up))
        btns.add_widget(Button(text="SELECT VIDEO", on_release=self.set_video))
        btns.add_widget(Button(text="SELECT AUDIO", on_release=self.set_audio))
        self.add_widget(btns)

        self.add_widget(Button(text="START MIX", size_hint_y=0.1, background_color=(0, 0.7, 0, 1), on_release=self.run_mix))

    def go_up(self, instance):
        # כפתור שיעזור לך לצאת מתיקיות ריקות חזרה למעלה
        self.file_chooser.path = os.path.dirname(self.file_chooser.path)

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = "Video OK!"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = "Audio OK!"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "Error: Select files!"
            return

        output_path = "/sdcard/Download/elazar_mix.mp4"
        if os.path.exists(self.ffmpeg_bin):
            os.chmod(self.ffmpeg_bin, os.stat(self.ffmpeg_bin).st_mode | stat.S_IEXEC)

        cmd = [
            self.ffmpeg_bin, "-y", "-i", self.video_path, "-i", self.audio_path,
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
        ]

        try:
            self.status_label.text = "Mixing..."
            subprocess.run(cmd, check=True)
            self.status_label.text = "Success! Saved in Downloads"
        except:
            self.status_label.text = "FFmpeg Error"

class ElazarEditorApp(App):
    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            # בקשת הרשאות בסיסיות
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            
            # ניסיון לפתוח את מסך "גישה לכל הקבצים" המיוחד של אנדרואיד 14
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Settings = autoclass('android.provider.Settings')
                Uri = autoclass('android.net.Uri')
                
                if not os.access('/sdcard', os.R_OK):
                    intent = Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
                    PythonActivity.mActivity.startActivity(intent)
            except:
                pass
                
        return VideoAudioMixer()

if __name__ == '__main__':
    ElazarEditorApp().run()
