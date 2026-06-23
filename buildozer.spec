[app]
title = Proeco Network Diagnostics
package.name = proeco_diagnostics
package.domain = mbathtech.it
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0

[app:permissions]
android.permissions = INTERNET,ACCESS_NETWORK_STATE

[app:android]
android.api = 31
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
