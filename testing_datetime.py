from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

image = Image.open("test_rename/2023-01-08_163153.jpg")

exifdata = image.getexif().get_ifd(0x8769)

for tag_id in exifdata:
    tag = TAGS.get(tag_id, tag_id)
    content = exifdata.get(tag_id)
    print(f"{tag:25}: {content}")

print(exifdata.get(36867))
creation = datetime.strptime(exifdata.get(36867), "%Y:%m:%d %H:%M:%S")
print(creation.month)
print(creation.year)
