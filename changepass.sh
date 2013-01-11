#!/bin/bash
#Usage: ./changepass.sh <username> <new password>
echo "changepass.sh"
expect << EOF
spawn passwd $1
expect "Enter new UNIX password:"
send "${2}\r"
expect "Retype new UNIX password:"
send "${2}\r"
expect eof;
EOF
