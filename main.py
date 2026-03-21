import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.utils import platform

# ייבוא FFmpegKit לאנדרואיד בלבד
if platform == 'android':
    from jnius import autoclass
    FFmpegKit = autoclass('com.ffmpegkit.FFmpegKit')
    ReturnCode = autoclass('com.ffmpegkit.ReturnCode')

class VideoAudioMixer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)
        
        self.video_path = None
        self.audio_path = None
        
        self.label = Label(text="ELAZAR EDITOR V3.2", font_size='24sp', size_hint_y=0.1)
        self.add_widget(self.label)
        
        self.status_label = Label(text="בחר וידאו ואז אודיו", size_hint_y=0.1)
        self.add_widget(self.status_label)
        
        # סייר קבצים
        default_path = '/sdcard' if platform == 'android' else os.path.expanduser("~")
        self.file_chooser = FileChooserIconView(path=default_path)
        self.add_widget(self.file_chooser)
        
        # כפתורים
        btns = BoxLayout(size_hint_y=0.2, spacing=10)
        self.btn_video = Button(text="1. בחר וידאו", on_release=self.set_video)
        self.btn_audio = Button(text="2. בחר אודיו", on_release=self.set_audio)
        self.btn_mix = Button(text="3. בצע MIX", background_color=(0.1, 0.8, 0.1, 1), on_release=self.run_mix)
        
        btns.add_widget(self.btn_video)
        btns.add_widget(self.btn_audio)
        btns.add_widget(self.btn_mix)
        self.add_widget(btns)

    def set_video(self, instance):
        if self.file_chooser.selection:
            self.video_path = self.file_chooser.selection[0]
            self.status_label.text = f"וידאו: {os.path.basename(self.video_path)}"

    def set_audio(self, instance):
        if self.file_chooser.selection:
            self.audio_path = self.file_chooser.selection[0]
            self.status_label.text = f"אודיו: {os.path.basename(self.audio_path)}"

    def run_mix(self, instance):
        if not self.video_path or not self.audio_path:
            self.status_label.text = "חובה לבחור 2 קבצים!"
            return

        # נתיב תיקיית היעד
        if platform == 'android':
            base_path = "/sdcard/Download/ELAZAR_DOWNLOADS"
        else:
            base_path = os.path.join(os.path.expanduser("~"), "Downloads", "ELAZAR_DOWNLOADS")

        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)

        output_path = os.path.join(base_path, "mixed_video.mp4")
        self.status_label.text = "מעבד... נא להמתין"
        
        # פקודת המיקס (החלפת אודיו ללא קידוד מחדש של הוידאו)
        command = f"-y -i '{self.video_path}' -i '{self.audio_path}' -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -shortest '{output_path}'"
        
        if platform == 'android':
            session = FFmpegKit.execute(command)
            if ReturnCode.isSuccess(session.getReturnCode()):
                self.status_label.text = "הצלחה! נשמר ב-ELAZAR_DOWNLOADS"
            else:
                self.status_label.text = "שגיאה במיקס"
        else:
            self.status_label.text = f"הדמיה: {output_path}"

class ElazarEditorApp(App):
    def build(self):
        return VideoAudioMixer()

if __name__ == '__main__':
    ElazarEditorApp().run()
