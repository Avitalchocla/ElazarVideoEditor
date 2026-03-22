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
        
        self.add_widget(Label(text="ELAZAR EDITOR V3.9", font_size='24sp', size_hint_y=0.1))
        
        # סייר קבצים עם מסנן רחב יותר (תומך גם באותיות גדולות)
        path = '/sdcard/Download' if platform == 'android' else os.path.expanduser("~")
        self.file_chooser = FileChooserIconView(
            path=path, 
            filters=['*.mp4', '*.MP4', '*.mp3', '*.MP3', '*.m4a', '*.M4A', '*.wav', '*.WAV']
        )
        self.add_widget(self.file_chooser)
        
        self.status_label = Label(text="Status: Ready", size_hint_y=0.1)
        self.add_widget(self.status_label)
        
        # שורת כפתורי שליטה
        btns = BoxLayout(size_hint_y=0.15, spacing=10)
        btns.add_widget(Button(text="REFRESH", on_release=self.refresh_files))
        btns.add_widget(Button(text="SELECT VIDEO", on_release=self.set_video))
        btns.add_widget(Button(text="SELECT AUDIO", on_release=self.set_audio))
        self.add_widget(btns)

        # כפתור המיקס הגדול
        self.btn_mix = Button(text="START MIXING", size_hint_y=0.1, background_color=(0, 0.7, 0, 1), on_release=self.run_mix)
        self.add_widget(self.btn_mix)

    def refresh_files(self, instance):
        self.file_chooser._update_files()
        self.status_label.text = "List Refreshed"

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = f"Video OK: {os.path.basename(self.video_path)}"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = f"Audio OK: {os.path.basename(self.audio_path)}"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "Select both files!"
            return

        output_dir = "/sdcard/Download/ELAZAR_EDITOR"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "final_mix.mp4")

        if os.path.exists(self.ffmpeg_bin):
            os.chmod(self.ffmpeg_bin, os.stat(self.ffmpeg_bin).st_mode | stat.S_IEXEC)

        cmd = [
            self.ffmpeg_bin, "-y", "-i", self.video_path, "-i", self.audio_path,
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
        ]

        try:
            self.status_label.text = "Processing..."
            subprocess.run(cmd, check=True)
            self.status_label.text = f"Success! Saved in Downloads/ELAZAR_EDITOR"
        except:
            self.status_label.text = "Error in FFmpeg"

class ElazarEditorApp(App):
    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_MEDIA_VIDEO,
                Permission.READ_MEDIA_AUDIO,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])
        return VideoAudioMixer()

if __name__ == '__main__':
    ElazarEditorApp().run()
