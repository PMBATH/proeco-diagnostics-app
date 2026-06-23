[app]

# (str) Title of your application
title = Proeco Network Diagnostics

# (str) Package name
package.name = proeco_diagnostics

# (str) Package domain (needed for android/ios packaging)
package.domain = mbathtech.it

# (source.dir) Source code directory
source.dir = .

# (list) Source include patterns (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source exclude patterns
#source.exclude_exts = spec

# (list) List of directory to exclude from the build
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,json2yaml
requirements = python3,kivy,requests

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_bgcolor = #FFFFFF

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 30

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) Use --private data storage (True) or --shared data storage (False)
#android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (int) overrides automatic versionCode computation from version.x.y.zeta for command line builds
# this is most useful for your continuous building systems if you don't want to run
# buildozer.android_debug each time when you build your project, depending on git commit number, etc.
# uncomment this option and set it this way ( just an example )
# android.release_artifact = aab

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup scheme, see the documentation
# android.backup_schemes = @xml/backup_scheme

# (str) The Android logcat filters to use when running `buildozer android logcat`
# android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (str) The presplash icon image path
#android.presplash = %(source.dir)s/data/presplash.png

# (str) The presplash animation file (NewVolumePercent:file.png) resolution = (320, 470)
#android.presplash_animation = %(source.dir)s/data/presplash_animation

# (str) Gradle dependencies (for android.gradle_dependencies)
#android.gradle_dependencies = com.google.android.material:material:1.1.0

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

# (str) Path to a custom whitelist file
#android.whitelist = ./whitelist.txt

# (bool) Disable PyVenv check during APK creation (useful if you don't use
# PyVenv in your project).
# android.skip_pyvenv_check = False

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Android logcat filters to use when running `buildozer android logcat`
# android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (str) The prespl icon image path
#android.presplash = %(source.dir)s/data/presplash.png

# (str) Gradle dependencies (for android.gradle_dependencies)
#android.gradle_dependencies =

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warnings (1) or not (0)
warn_on_root = 1
