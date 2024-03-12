# Access Control
## Background knowledge
- copy content of a file: `cp --copy-content <SRC_FILE> <DST_FILE>`
- join a group with password: `newgrp <GROUP_NAME>`, then type in the password. The `newgrp` command is typically used to switch the primary group of the current user to another existing group, if the user is not already a member of the specified group, `newgrp` will prompt for the password of the group
- know which users are in a given group: `getent group <GROUP_NAME>`
- search for a keyword in all files inside a directory: `grep -r <KEYWORD> <DIRECTORY>`
## Challenges
- nothing difficult, the last few challenges require us to write a program to automate the answering process
