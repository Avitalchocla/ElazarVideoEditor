from kivy.app import App
from kivy.lang import Builder
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy.clock import Clock
import os

class VideoEditorApp(App):
    def build(self):
        self.title = "ELAZAR EDITOR"
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])
        return Builder.load_file("ui.kv")

    def open_file_manager(self, target_id):
        # יצירת חלונית בחירת קבצים
        content = FileChooserIconView(path='/storage/emulated/0/')
        popup = Popup(title="Select File", content=content, size_hint=(0.9, 0.9))
        
        def on_selection(instance, selection):
            if selection:
                if target_id == 'video':
                    self.root.ids.vid_input.text = selection[0]
                else:
                    self.root.ids.aud_input.text = selection[0]
                popup.dismiss()

        content.bind(on_submit=on_selection)
        popup.open()

    def start_processing(self):
        v = self.root.ids.vid_input.text
        a = self.root.ids.aud_input.text
        if not v or not a:
            self.root.ids.status.text = "❌ Please select both files"
            return
        
        self.root.ids.status.text = "🔄 Processing... (Check ELAZAR_EDITED folder soon)"
        # כאן תבוא פקודת ה-FFmpeg בשלב הבא
