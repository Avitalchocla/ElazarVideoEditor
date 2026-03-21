[app]
title = ELAZAR EDITOR
package.name = ezedit
package.domain = org.elazar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.4

# הורדתי את ffmpeg-kit מהדרישות, נשתמש בבינארי
requirements = python3,kivy==2.3.0

orientation = portrait
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO

android.api = 33
android.minapi = 21
# איחוד גרסאות NDK לפי הצעתך
android.ndk = 25b
android.build_tools_version = 33.0.0
android.archs = arm64-v8a

android.accept_sdk_license = True
android.enable_androidx = True

android.allow_backup = True
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
