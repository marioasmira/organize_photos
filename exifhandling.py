from PIL import Image
from datetime import datetime
import exiftool

# sometimes a first layer doesn't work so we need a different tag?
EXIF_TAG_ID_DATETIME = 306
EXIF_TAG_ID_DATETIME_ALT = 36867

# Exception for when the file doesn't have creation time metadata
class NoDatetimeFound(Exception):
    "Didn't find information about creation time."
    pass


def extract_from_image(file_location) -> datetime:
    # read the image data using PIL
    image = Image.open(file_location)

    try:
        # extract EXIF data
        exifdata = image.getexif()
        time_string = str(exifdata.get(EXIF_TAG_ID_DATETIME))
        creation = datetime.strptime(time_string, "%Y:%m:%d %H:%M:%S")

    except (TypeError, ValueError):
        try:
            # extract EXIF data
            exifdata = image.getexif().get_ifd(0x8769)
            time_string = str(exifdata.get(EXIF_TAG_ID_DATETIME_ALT))
            creation = datetime.strptime(time_string, "%Y:%m:%d %H:%M:%S")

        except (TypeError, ValueError):
            raise NoDatetimeFound

    finally:
        # need to close the image to move it afterwards
        image.close()

    return creation


def extract_from_video(file_location) -> datetime:
    try:
        # extract EXIF data
        with exiftool.ExifToolHelper() as et:
            exifdata = et.get_metadata(file_location)
        time_string = exifdata[0]["EXIF:DateTimeOriginal"]
        creation = datetime.strptime(time_string, "%Y:%m:%d %H:%M:%S")

    except (TypeError, KeyError):
        try:
            # extract EXIF data
            with exiftool.ExifToolHelper() as et:
                exifdata = et.get_metadata(file_location)
            time_string = exifdata[0]["QuickTime:CreateDate"]
            creation = datetime.strptime(time_string, "%Y:%m:%d %H:%M:%S")

        except (TypeError, KeyError):
            raise NoDatetimeFound

    return creation
