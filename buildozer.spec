[app]
title = ELAZAR EDITOR
package.name = elazareditor
package.domain = org.elazar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.2

# דרישות מינימליות למניעת קריסות
requirements = python3,kivy==2.3.0,requests,certifi

orientation = portrait

# הרשאות ניהול קבצים
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# שימוש ב-API 30 ליציבות מקסימלית
android.api = 30
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# משיכת FFmpeg Kit דרך Gradle
android.gradle_dependencies = "com.artyomd.ffmpeg:ffmpeg-kit-full:4.5"

android.allow_backup = True
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
