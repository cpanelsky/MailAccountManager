Mail Account Manager for WHM
============================
Alpha - use at your own risk!
-------------------------------

sha512sum: d84f7e0efb15ddb570e16b0d525c8c019919d14113ba8915d9b9395242932d3d428c5f437341b6a62e163e973aa6ff2bdbc364e8e0e53daba2e3dd229f0c3e59  MailAccountManager-0.01-0.01.x86_64.rpm

### Video Demo:

https://www.youtube.com/watch?v=-uoa6hhKxgQ

### Features:

- cPanel account actions use the new WHM mail suspend features, e-mail account actions call the cPanel mail API commands through json-uapi.

### Installation:

yum localinstall  https://github.com/cpanelsky/MailAccountManager/raw/master/MailAccountManager-0.01-0.01.x86_64.rpm

### Manual Installation:

git clone https://github.com/cpanelsky/MailAccountManager.git
cd MailAccountManager/rpmbuild/SOURCES/MailAccountManager-0.01
./installer 
