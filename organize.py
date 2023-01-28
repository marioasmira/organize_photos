from PIL import Image
from PIL.ExifTags import TAGS
import os
import sys
import exiftool

EXIF_TAG_ID_DATETIME = 306
EXIF_TAG_ID_DATETIME_ALT = 36867

# creation date
class C_date:
    year = "5000"
    month = "13"
    def __init__(self) -> None:
        pass

def extract_from_image(file_location) -> C_date:

    creation = C_date

    # read the image data using PIL
    image = Image.open(file_location)


    try:
        # extract EXIF data
        exifdata = image.getexif()
        creation.year = exifdata.get(EXIF_TAG_ID_DATETIME)[:4]
        creation.month = exifdata.get(EXIF_TAG_ID_DATETIME)[5:7]

    except TypeError:
        try:
            # extract EXIF data
            exifdata = image.getexif().get_ifd(0x8769)
            creation.year = exifdata.get(EXIF_TAG_ID_DATETIME_ALT)[:4]
            creation.month = exifdata.get(EXIF_TAG_ID_DATETIME_ALT)[5:7]

        except TypeError:
            print("Photo", file_location, "appears to have no metadata.")
            creation.year = "5000"
            creation.month = "13"

    # need to close the image to move it afterwards
    image.close()

    return creation

def extract_from_video(file_location) -> C_date:

    creation = C_date

    try:
        # extract EXIF data
        with exiftool.ExifToolHelper() as et:
            exifdata = et.get_metadata(file_location)
        creation.year = exifdata[0]["EXIF:DateTimeOriginal"][:4]
        creation.month = exifdata[0]["EXIF:DateTimeOriginal"][5:7]

    except (TypeError, KeyError):
        try:
            # extract EXIF data
            with exiftool.ExifToolHelper() as et:
                exifdata = et.get_metadata(file_location)
            creation.year = exifdata[0]["QuickTime:CreateDate"][:4]
            creation.month = exifdata[0]["QuickTime:CreateDate"][5:7]

        except (TypeError, KeyError):
            print("Video", file_location, "appears to have no metadata.")
            creation.year = "5000"
            creation.month = "13"

    return creation

def main(argv):
    print(argv)
    if (len(argv) <= 1):
        print("The script needs the target folder location.")
        sys.exit()

    # path to the image or video
    folder = argv[1]
    if not (folder[-1] == "/"):
        folder = folder + "/"
    if (not os.path.exists(folder)):
        print("Can not find the specified folder:", folder)
        sys.exit()

    for file in os.listdir(folder):
        if (file.endswith(".jpg") or
        file.endswith(".JPG") or
        file.endswith(".mp4") or
        file.endswith(".MP4") or
        file.endswith(".3gp")):

            imagename = file
            file_location = folder + imagename

            if (file.endswith(".jpg") or file.endswith(".JPG")):
                creation_date = extract_from_image(file_location)
            else:
                creation_date = extract_from_video(file_location)

            if (creation_date.year != "5000" and creation_date.month != "13"):
                top_new_path = creation_date.year + "/"
                if(not os.path.exists(top_new_path)):
                    os.mkdir(top_new_path)

                new_path = top_new_path + creation_date.month + "/"
                if(not os.path.exists(new_path)):
                    os.mkdir(new_path)
            else:
                new_path = "no_metadata/"
                if(not os.path.exists(new_path)):
                    os.mkdir(new_path)

            if(os.path.isfile(file_location) and not os.path.isfile(new_path + imagename)):
                os.rename(file_location, new_path + imagename)
            else:
                print("Skipping file", new_path + imagename, ": it already exists in the target folder.")

if __name__ == "__main__":
    main(sys.argv)