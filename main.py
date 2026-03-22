import os
import subprocess
import stat
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.utils import platform
from kivy.clock import Clock

# פונקציה לבקשת הרשאות באנדרואיד (מותאם לאנדרואיד 13+)
def request_android_permissions():
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        permissions = [
            Permission.READ_MEDIA_VIDEO,
            Permission.READ_MEDIA_AUDIO,
            Permission.READ_MEDIA_IMAGES,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ]
        request_permissions(permissions)

class VideoAudioMixer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)
        
        # בקשת הרשאות מיד עם פתיחת האפליקציה
        Clock.schedule_once(lambda dt: request_android_permissions(), 1)

        # איתור ה-FFmpeg (הקוד הקודם שלך עבד מצוין)
        self.ffmpeg_bin = os.path.join(os.path.dirname(__file__), "ffmpeg")
        
        # מתן הרשאות הרצה
        if os.path.exists(self.ffmpeg_bin):
            try:
                st = os.stat(self.ffmpeg_bin)
                os.chmod(self.ffmpeg_bin, st.st_mode | stat.S_IEXEC)
            except:
                pass

        self.video_path = None
        self.audio_path = None
        
        # שינוי טקסטים לאנגלית למניעת ג'יבריש
        self.label = Label(text="ELAZAR EDITOR PRO", font_size='24sp', size_hint_y=0.1)
        self.add_widget(self.label)
        
        self.status_label = Label(text="Welcome", size_hint_y=0.1)
        self.add_widget(self.status_label)
        
        # ניסיון גישה לתיקיית הסרטים
        if platform == 'android':
            default_path = '/sdcard/Movies'
            if not os.path.exists(default_path):
                default_path = '/sdcard'
        else:
            default_path = os.path.expanduser("~")
            
        self.file_chooser = FileChooserIconView(path=default_path)
        self.add_widget(self.file_chooser)
        
        btns = BoxLayout(size_hint_y=0.2, spacing=10)
        self.btn_video = Button(text="1. SELECT VIDEO", on_release=self.set_video)
        self.btn_audio = Button(text="2. SELECT AUDIO", on_release=self.set_audio)
        self.btn_mix = Button(text="3. RUN MIX", background_color=(0, 0.8, 0, 1), on_release=self.run_mix)
        
        btns.add_widget(self.btn_video)
        btns.add_widget(self.btn_audio)
        btns.add_widget(self.btn_mix)
        self.add_widget(btns)

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = f"VIDEO SELECTED"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = f"AUDIO SELECTED"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "Error: Select 2 files first!"
            return

        base_path = "/sdcard/Download/ELAZAR_DOWNLOADS" if platform == 'android' else "./"
        os.makedirs(base_path, exist_ok=True)
        output_path = os.path.join(base_path, "mixed_result.mp4")

        self.status_label.text = "Mixing... please wait"

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
            self.status_label.text = "SUCCESS! Check ELAZAR_DOWNLOADS"
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

class ElazarEditorApp(App):
    def build(self):
        return VideoAudioMixer()

if __name__ == '__main__':
    ElazarEditorApp().run()
