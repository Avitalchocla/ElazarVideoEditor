[app]

# (str) Title of your application
title = ELAZAR EDITOR

# (str) Package name
package.name = elazareditor

# (str) Package domain (needed for android packaging)
package.domain = org.elazar

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.1

# (list) Application requirements
# הוספנו את hostpython3 ו-ffpyplayer שקריטיים לעריכת וידאו
requirements = python3,hostpython3,kivy==2.3.0,ffmpeg,ffpyplayer,requests,certifi

# (str) Supported orientations
orientation = portrait

# (list) Permissions
# הרשאות מורחבות לניהול קבצים באנדרואיד
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 31

# (str) Android NDK version to use
android.ndk = 25b

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) indicates if the application should be etched for the targets
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab)
android.debug_artifact = apk

# (list) Gradle dependencies
# לעיתים נדרש עבור ffmpeg-kit
# android.gradle_dependencies = com.artyomd.ffmpeg:ffmpeg-kit-full:4.5

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
