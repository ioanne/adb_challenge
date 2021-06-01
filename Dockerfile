FROM gradle:4.10.0-jdk8

USER root

ENV SDK_URL="https://dl.google.com/android/repository/sdk-tools-linux-3859397.zip" \
    ANDROID_HOME="/usr/local/android-sdk" \
    ANDROID_VERSION=28 \
    ANDROID_BUILD_TOOLS_VERSION=27.0.3

# Download Android SDK
RUN mkdir "$ANDROID_HOME" .android \
    && cd "$ANDROID_HOME" \
    && curl -o sdk.zip $SDK_URL \
    && unzip sdk.zip \
    && rm sdk.zip \
    && mkdir "$ANDROID_HOME/licenses" || true \
    && echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > "$ANDROID_HOME/licenses/android-sdk-license"


# Install Android Build Tool and Libraries
RUN $ANDROID_HOME/tools/bin/sdkmanager --update
RUN mkdir -p /root/.android && touch /root/.android/repositories.cfg
RUN $ANDROID_HOME/tools/bin/sdkmanager "build-tools;${ANDROID_BUILD_TOOLS_VERSION}" \
    "platforms;android-${ANDROID_VERSION}" \
    "platform-tools"

RUN apt update
RUN apt install -y --no-install-recommends software-properties-common
RUN apt install -y --no-install-recommends python3-pip
RUN apt install -y --no-install-recommends build-essential file apt-utils curl gettext libjpeg-dev python3-dev && \
    apt install -y --no-install-recommends gcc libffi-dev gdal-bin && \
    apt autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install python dependencies
FROM python:3.9.2-slim-buster
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

# add app
COPY . .