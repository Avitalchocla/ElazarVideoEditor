[app]

# (str) Title of your application
title = ELAZAR EDITOR

# (str) Package name (קיצור השם למניעת שגיאת נתיב ארוך)
package.name = ezedit

# (str) Package domain
package.domain = org.elazar

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.4

# (list) Application requirements
# הוספת ffmpeg ו-ffpyplayer בצורה יציבה
requirements = python3,kivy==2.3.0,ffmpeg,ffpyplayer,requests,certifi

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) Android architectures to build for
# השארנו רק אחת כדי למנוע את השגיאה שקיבלת ב-GitHub
android.archs = arm64-v8a

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (str) Android additionnal libraries
android.gradle_dependencies = "com.artyomd.ffmpeg:ffmpeg-kit-full:4.5"

# (bool) indicates if the application should be etched for the targets
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
