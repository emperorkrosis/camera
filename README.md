# Security Camera Repository
## Motivation
The motivation of this project is to create a simple security camera detection tool for my house. This project does not follow best practices and is easily "defeatable" so *caveat emptor*.

Currently, this script is fairly simple and performs the following steps:

1. Grab the current camera image from the security camera over the LAN.
2. Compare the image against the previous one to find the RMS error.
3. If the error is greater than a certain threshold then save the image.
4. Repeat every 1 second.

## Installation
To use this tool:

1. Download record.py and record.sh to a directory on your machine.
2. Create a ./data subdirectory.
3. Edit record.sh to pass the correct password in.
4. Run record.sh.

## Future Work
The following items are future work:

- Smarter detection of faces/people in the images.
- Scheduling so we only detect when someone is not at home.
- Notifications for when something is detected: Email or SMS.
- Improved robustness against different classes of false positives.
