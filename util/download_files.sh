#!/bin/bash
#
# Script: download_files.sh
# Description: This script reads URLs from a file and uses wget to download them with specified cookies.
# Author: Nicolas Souza
# Date: August 29, 2023
#
# Usage: ./download_files.sh
#

# Replace the following variable with the actual cookies from your session
cookies=""

filename="files"

if [ -f "$filename" ]; then
  while IFS= read -r line; do
    echo "Line: $line"
    wget --header "Cookie: $cookies" "$line"   
  done < "$filename"
else
  echo "File $filename not found."
fi

