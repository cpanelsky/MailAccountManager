#!/bin/bash
/usr/sbin/whmapi1 create_user_session service=webmaild user=$@ | grep -oP '(?<=url: ).*(?=$)'
