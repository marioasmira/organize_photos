from PIL import Image
from PIL.ExifTags import TAGS

def print_exif_data(exif_data):
    for tag_id in exif_data:
        tag = TAGS.get(tag_id, tag_id)
        content = exif_data.get(tag_id)
        print(f'{tag:25}: {content}')

with Image.open("test_rename/IMG_5599.JPG") as im:
    exif = im.getexif()
    
    print_exif_data(exif)
    print_exif_data(exif.get_ifd(0x8769))