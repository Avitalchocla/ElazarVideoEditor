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
        
        self.add_widget(Label(text="ELAZAR EDITOR V4.3", font_size='24sp', size_hint_y=0.1))
        
        # סייר קבצים משופר - מציג הכל
        path = '/sdcard' if platform == 'android' else os.path.expanduser("~")
        self.file_chooser = FileChooserIconView(
            path=path,
            filters=['*.mp4', '*.MP4', '*.mp3', '*.MP3', '*.m4a', '*.M4A', '*.wav', '*.WAV'],
            dirselect=False
        )
        self.add_widget(self.file_chooser)
        
        self.status_label = Label(text="If empty: Press REFRESH and check 'All Files Access'", size_hint_y=0.1)
        self.add_widget(self.status_label)
        
        # שורת כפתורי שליטה
        btns = BoxLayout(size_hint_y=0.2, spacing=10)
        btns.add_widget(Button(text="FORCE REFRESH", on_release=self.force_refresh))
        btns.add_widget(Button(text="SET VIDEO", on_release=self.set_video))
        btns.add_widget(Button(text="SET AUDIO", on_release=self.set_audio))
        self.add_widget(btns)

        self.add_widget(Button(text="START MIXING", size_hint_y=0.1, background_color=(0, 0.7, 0, 1), on_release=self.run_mix))

    def force_refresh(self, instance):
        # פקודה שמכריחה את סייר הקבצים לסרוק מחדש את התיקייה הנוכחית
        current_path = self.file_chooser.path
        self.file_chooser.path = '/' 
        self.file_chooser.path = current_path
        self.status_label.text = "Scanning folder..."

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = f"VIDEO: {os.path.basename(self.video_path)}"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = f"AUDIO: {os.path.basename(self.audio_path)}"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "Error: Select 2 files first!"
            return

        output_path = "/sdcard/Download/final_output.mp4"
        if os.path.exists(self.ffmpeg_bin):
            os.chmod(self.ffmpeg_bin, os.stat(self.ffmpeg_bin).st_mode | stat.S_IEXEC)

        cmd = [
            self.ffmpeg_bin, "-y", "-i", self.video_path, "-i", self.audio_path,
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
        ]

        try:
            self.status_label.text = "Processing... Please wait"
            subprocess.run(cmd, check=True)
            self.status_label.text = "SUCCESS! Check Downloads folder"
        except:
            self.status_label.text = "FFmpeg Failed"

class ElazarEditorApp(App):
    def build(self):
        return VideoAudioMixer()

if __name__ == '__main__':
    ElazarEditorApp().run()
