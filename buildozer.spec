[app]
title = Video Downloader
package.name = videodownloader
package.domain = org.mydownloader
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Các thư viện Python ứng dụng sử dụng
requirements = python3,kivy==2.3.0,yt-dlp,requests,urllib3,certifi

# Cấu hình Android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
