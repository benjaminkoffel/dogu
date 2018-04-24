brew update
brew install npm
brew install watchman
brew cask install android-studio
export ANDROID_HOME=/Users/$USER/Library/Android/sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export PATH=$ANDROID_SDK_ROOT/tools:$PATH
export PATH=$ANDROID_SDK_ROOT/tools/bin:$PATH
sdkmanager --update
sdkmanager "system-images;android-23;google_apis;x86"
sdkmanager --licenses
avdmanager create avd -n test -k "system-images;android-23;google_apis;x86" -b x86 -c 100M -d 7 -f
emulator -avd test
npm install -g create-react-native-app
npm install -g react-native-cli
# npm install react-native-camera --save
# react-native link react-native-camera