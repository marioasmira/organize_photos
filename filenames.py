import os
import exifhandling


def extract_date_time(file, file_location) -> tuple:
    # extract the day and time a file was created
    try:
        if file.endswith(".jpg") or file.endswith(".JPG"):
            creation_date = exifhandling.extract_from_image(file_location)
        else:
            creation_date = exifhandling.extract_from_video(file_location)

        # rename if there is metadata
        file_name = (
            creation_date.strftime("%Y-%m-%d_%H%M%S") + os.path.splitext(file)[1]
        )

        return file_name, True

    # when there is no metadata, move to single folder
    except exifhandling.NoDatetimeFound:
        print("File", file_location, "appears to have no metadata. Skipping!")
        return "_", False
