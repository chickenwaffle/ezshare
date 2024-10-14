#!/usr/bin/env python
######################################################################
# ezshare.py - Upload a file to your server and obfuscate the filename
# Dependencies: paramiko pyperclip
######################################################################
# Author:  kornflakes
# Date:    March 2024
# License: MIT License 2024
#          https://mit-license.org/
######################################################################

import paramiko   #SSH operations - paramiko.SSHClient(), paramiko.AutoAddPolicy()
import hashlib    #hashlib.sha256()
import pyperclip  #clipboard - pyperclip.copy()
from urllib.parse import quote #creates browser-friendly links - quote_plus()
import sys        #get arguments - sys.argv[]
import os         #file name operations - os.path.basename(), os.path.splitext()


#################
# - Variables - #
#################
#
# THE FOLLOWING VARIABLES *MUST* BE CHANGED TO MATCH YOUR SYSTEMS.
#
# Set WEBSITE_PATH to the public destination *directory* for the
#   file to go (i.e. www.user.com/images/)
#
# BE SURE TO INCLUDE THE FORWARD-SLASH AT THE END "/"
#
# Do not use your local IP address.  This website should be
#   accessible to others outside of your local network.
WEBSITE_PATH    = "www.publicwebsite.com/path/to/destination/"
FILESYSTEM_PATH = "/var/www/path/to/same/destination/"

# Either "http" or "https"
PROTOCOL = "https"

# SSH Information - SCP will use this to upload your file to your server
SSH_ADDRESS     = "put.ssh.ip.here"
SSH_PORT        = 22
SSH_USERNAME    = "sshuser"
SSH_PASSWORD    = "sshpassword"



#################
# - Functions - #
#################

# Define the SCP upload function
def scp_upload(host, port, username, password, local_file, remote_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(host, port, username, password)

    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_path)
    sftp.close()

    ssh.close()


def encryptAndUpload():
    # Get the file path from the command line argument
    file_path = sys.argv[1]

    # Get the file name
    file_full_name = os.path.basename(file_path)

    # Split the name and extension for hashing later
    file_name, file_extension = os.path.splitext(file_full_name)

    # Convert the file to a hash
    BLOCK_SIZE = 65536
    file_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)

    hashed_name = file_hash.hexdigest()

    # Define the remote path where the file will be uploaded
    remote_path = FILESYSTEM_PATH + f'{hashed_name + file_extension}'

    # Call the SCP upload function
    print("Uploading to", WEBSITE_PATH)
    scp_upload(SSH_ADDRESS, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, file_path, remote_path)

    # Copy the shareable link to your clipboard
    pyperclip.copy(PROTOCOL + "://" + WEBSITE_PATH + hashed_name + file_extension)
    print("Done. Link has been copied to clipboard.")


def uploadAsIs():
    # Get the file path from the command line argument
    file_path = sys.argv[1]

    # Get the file name
    file_full_name = os.path.basename(file_path)

    # Define the remote path where the file will be uploaded
    remote_path = FILESYSTEM_PATH + file_full_name

    # Call the SCP upload function
    print("Uploading to", WEBSITE_PATH)
    scp_upload(SSH_ADDRESS, SSH_PORT, SSH_USERNAME, SSH_PASSWORD, file_path, remote_path)

    # Copy the shareable link to your clipboard
    unclean_link = PROTOCOL + "://" + WEBSITE_PATH + file_full_name
    url_friendly_link = quote(unclean_link, ':/')
    pyperclip.copy(url_friendly_link)
    print("Done. Link has been copied to clipboard.")


def display_menu():
    print("\nezshare")
    print("1. Encrypt filename and upload")
    print("2. Upload as is")
    print("3. Exit")


def main():
    # Exit if no argument is supplied
    if len(sys.argv) < 2:
        print("Usage: kornshare.py <filename>")
        sys.exit(1)

    # The menu loop
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            encryptAndUpload()
            break
        elif choice == '2':
            uploadAsIs()
            break
        elif choice == '3':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, please choose again.")


if __name__ == "__main__":
    main()
