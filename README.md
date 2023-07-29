# organize_photos

A simple Python script that reads image and video file metadata (jpg, JPG, mp4, MP4, and 3gp) and organizes them into year and month folders.
The script also renames them into the read date and time if present.

Requires the Pillow and pyexiftool packages and whatever those require!

## Usage

Use `python rename.py FOLDER_WITH_FILES` to rename all the files (with the prewritten extensions) in the folder. If there is more than one file with the same name (from sports mode in a camera for example) there will be added `_x` at the end of the file, where the x is a number.

Use `python organize.py FOLDER_WITH_FILES` to move all the files into folders with the year and subfolders with the month number at the same level as you run the script. This script **does not** work well with the `_x` system from `rename.py` yet. Some manual organization might be necessary.