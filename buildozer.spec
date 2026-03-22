[app]
title = ELAZAR EDITOR PRO
package.name = ezedit
package.domain = org.elazar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ffmpeg
version = 3.5

requirements = python3,kivy==2.3.0

orientation = portrait
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO, READ_MEDIA_AUDIO, READ_MEDIA_IMAGES

android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.0
android.archs = arm64-v8a

android.accept_sdk_license = True
android.enable_androidx = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
