[app]

title = Biblioteca de Casais

package.name = bibliotecacasais
package.domain = com.croger

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,pdf,doc,docx,htm,html

source.exclude_dirs = .git,.github,.buildozer,bin

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0


# =========================================================
# ANDROID
# =========================================================

android.api = 36

android.minapi = 24

android.ndk = 29

android.archs = arm64-v8a

android.sdk_path = /home/runner/android-sdk

android.accept_sdk_license = True


# =========================================================
# FILEPROVIDER
# =========================================================

android.add_src = android_src

android.add_resources = android_res

android.gradle_dependencies = androidx.core:core:1.13.1

android.enable_androidx = True



# =========================================================
# PYTHON-FOR-ANDROID
# =========================================================

p4a.branch = develop

p4a.extra_args = --extra-manifest-application-xml='<provider xmlns:android="http://schemas.android.com/apk/res/android" android:name="com.croger.bibliotecacasais.BibliotecaFileProvider" android:authorities="com.croger.bibliotecacasais.fileprovider" android:exported="false" android:grantUriPermissions="true"> <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths" /> </provider>'


[buildozer]

log_level = 2

warn_on_root = 1
