from PIL import Image
from PIL.ExifTags import TAGS
import os
import sys
import exiftool
from datetime import datetime

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


def main(argv):
    print(argv)
    if len(argv) <= 1:
        print("The script needs the target folder location.")
        sys.exit()

    # path to the image or video
    folder = argv[1]
    if not (folder[-1] == "/"):
        folder = folder + "/"
    if not os.path.exists(folder):
        print("Can not find the specified folder:", folder)
        sys.exit()

    # search for image or video files
    for file in os.listdir(folder):
        if (
            file.endswith(".jpg")
            or file.endswith(".JPG")
            or file.endswith(".mp4")
            or file.endswith(".MP4")
            or file.endswith(".3gp")
        ):

            file_name = file
            file_location = folder + file_name

            # extract the day and time a file was created
            try:
                if file.endswith(".jpg") or file.endswith(".JPG"):
                    creation_date = extract_from_image(file_location)
                else:
                    creation_date = extract_from_video(file_location)

                file_name = (
                    creation_date.strftime("%Y%m%d_%H%M%S") + os.path.splitext(file)[1]
                )

                top_new_path = str(creation_date.year) + "/"
                if not os.path.exists(top_new_path):
                    os.mkdir(top_new_path)

                new_path = top_new_path + str(creation_date.month).zfill(2) + "/"
                if not os.path.exists(new_path):
                    os.mkdir(new_path)

            except NoDatetimeFound:
                print("File", file_location, "appears to have no metadata.")
                new_path = "no_metadata/"
                if not os.path.exists(new_path):
                    os.mkdir(new_path)

            if os.path.isfile(file_location) and not os.path.isfile(
                new_path + file_name
            ):
                os.rename(file_location, new_path + file_name)
            else:
                print(
                    "Skipping file",
                    new_path + file_name,
                    ": it already exists in the target folder.",
                )


if __name__ == "__main__":
    main(sys.argv)
