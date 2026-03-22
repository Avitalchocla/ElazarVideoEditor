[app]
title = ELAZAR EDITOR
package.name = ezedit
package.domain = org.elazar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ffmpeg
version = 4.0

# הוספתי כאן את android - זה קריטי למניעת קריסה!
requirements = python3,kivy==2.3.0,android

orientation = portrait
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
