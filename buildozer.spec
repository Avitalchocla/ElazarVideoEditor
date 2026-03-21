[app]
title = ELAZAR EDITOR
package.name = elazareditor
package.domain = org.elazar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.3

# הוספתי כאן את הדרישה ל-FFmpeg בצורה ש-Buildozer מבין
requirements = python3,kivy==2.3.0,ffmpeg,ffpyplayer,requests,certifi

orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# שים לב לשורה הזו - היא קריטית לחיבור הוידאו
android.gradle_dependencies = "com.artyomd.ffmpeg:ffmpeg-kit-full:4.5"

[buildozer]
log_level = 2
warn_on_root = 1
