Mail Account Manager for WHM
============================

Alpha - use at your own risk!
-------------------------------

### Video Demo:

https://www.youtube.com/watch?v=-uoa6hhKxgQ

### Features:

- cPanel account actions use the new WHM mail suspend features, e-mail account actions call the cPanel mail API commands through json-uapi.

### Installation:

    wget https://github.com/cpanelsky/MailAccountManager/raw/master/dist/MailAccountManager.tar.xz
    echo 'de0a0d435d00aa6655ffd2ef8121ee63e5f9784df3a3b5f521e0afe3eb2a14f857ceeb1260738c99c09a4f0089c00142857bc377d7e9ce59209df4e62a351729  MailAccountManager-0.0.1a.tar.xz' | sha512sum --check
    tar -xf MailAccountManager.tar.xz;
    cd MailAccountManager;
    chmod +x ./install;
    ./install;
