from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
import os

# הגדרת נתיב לשמירה
OUTPUT_PATH = "/storage/emulated/0/Download/ELAZAR_EDITED/"

class VideoEditorApp(App):
    video_path = ""
    audio_path = ""

    def build(self):
        self.title = "ELAZAR VIDEO EDITOR"
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.READ_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])
        return Builder.load_file("ui.kv")

    def select_video(self):
        # במערכת אמיתית נשתמש ב-filechooser, כרגע נבקש נתיב או נשתמש בקיים מהורדות
        self.update_status("Select Video feature coming soon...")
        # כאן נשלב בהמשך את plyer.filechooser

    def start_processing(self):
        v = self.root.ids.vid_input.text
        a = self.root.ids.aud_input.text
        
        if not v or not a:
            self.update_status("❌ Please enter both paths")
            return

        self.update_status("🔄 Processing Video... Please wait")
        
        if platform == 'android':
            self.run_ffmpeg_android(v, a)
        else:
            self.update_status("❌ FFmpeg runs only on Android/Linux")

    def run_ffmpeg_android(self, v_path, a_path):
        import threading
        def run():
            try:
                if not os.path.exists(OUTPUT_PATH):
                    os.makedirs(OUTPUT_PATH)
                
                out_file = os.path.join(OUTPUT_PATH, "output_combined.mp4")
                
                # פקודת ה-FFmpeg המנצחת: החלפת אודיו
                # -map 0:v (לוקח וידאו מהראשון) -map 1:a (לוקח אודיו מהשני)
                cmd = f"-i {v_path} -i {a_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest {out_file}"
                
                from ffmpeg_kit_flutter import FFmpegKit # דוגמה לספרייה
                # כאן נשתמש ב-subprocess או ב-jnius לקריאה ל-FFmpeg-Kit
                
                Clock.schedule_once(lambda dt: self.update_status(f"✅ Done! Saved to ELAZAR_EDITED"))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_status(f"❌ Error: {str(e)}"))

        threading.Thread(target=run).start()

    def update_status(self, text):
        self.root.ids.status.text = text

if __name__ == "__main__":
    VideoEditorApp().run()