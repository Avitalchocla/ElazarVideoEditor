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
        
        # איתור ה-FFmpeg שהורדנו ב-Workflow
        self.ffmpeg_bin = os.path.join(os.path.dirname(__file__), "ffmpeg")
        
        # מתן הרשאות הרצה (קריטי לאנדרואיד)
        if os.path.exists(self.ffmpeg_bin):
            try:
                st = os.stat(self.ffmpeg_bin)
                os.chmod(self.ffmpeg_bin, st.st_mode | stat.S_IEXEC)
            except:
                pass

        self.video_path = None
        self.audio_path = None
        
        self.label = Label(text="ELAZAR EDITOR V3.5", font_size='24sp', size_hint_y=0.1)
        self.add_widget(self.label)
        
        self.status_label = Label(text="מוכן לעבודה", size_hint_y=0.1)
        self.add_widget(self.status_label)
        
        default_path = '/sdcard' if platform == 'android' else os.path.expanduser("~")
        self.file_chooser = FileChooserIconView(path=default_path)
        self.add_widget(self.file_chooser)
        
        btns = BoxLayout(size_hint_y=0.2, spacing=10)
        self.btn_video = Button(text="1. בחר וידאו", on_release=self.set_video)
        self.btn_audio = Button(text="2. בחר אודיו", on_release=self.set_audio)
        self.btn_mix = Button(text="3. בצע MIX", background_color=(0, 0.8, 0, 1), on_release=self.run_mix)
        
        btns.add_widget(self.btn_video)
        btns.add_widget(self.btn_audio)
        btns.add_widget(self.btn_mix)
        self.add_widget(btns)

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = f"וידאו נבחר בהצלחה"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = f"אודיו נבחר בהצלחה"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "חובה לבחור שני קבצים!"
            return

        base_path = "/sdcard/Download/ELAZAR_DOWNLOADS" if platform == 'android' else "./"
        os.makedirs(base_path, exist_ok=True)
        output_path = os.path.join(base_path, "mixed_result.mp4")

        self.status_label.text = "מבצע מיקס... נא להמתין"

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
            self.status_label.text = "הצלחה! הקובץ בתיקיית ELAZAR_DOWNLOADS"
        except Exception as e:
            self.status_label.text = f"שגיאה: {str(e)}"

class ElazarEditorApp(App):
    def build(self):
        return VideoAudioMixer()

if __name__ == '__main__':
    ElazarEditorApp().run()
