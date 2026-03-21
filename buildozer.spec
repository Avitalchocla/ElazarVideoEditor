[app]
title = ELAZAR EDITOR
package.name = ezedit
package.domain = org.elazar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.4

requirements = python3,kivy==2.3.0,requests

orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.ndk = 25c
android.archs = arm64-v8a

# הוספת הגדרות למניעת עדכונים אוטומטיים ששוברים את ה-build
android.skip_update = True
android.accept_sdk_license = True

# שימוש ב-FFmpegKit
android.gradle_dependencies = com.artyomd.ffmpeg:ffmpeg-kit-full:4.5

android.allow_backup = True
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
