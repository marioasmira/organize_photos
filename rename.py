import os
import sys
import organize


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
                    creation_date = organize.extract_from_image(file_location)
                else:
                    creation_date = organize.extract_from_video(file_location)

                # rename if there is metadata
                file_name = (
                    creation_date.strftime("%Y-%m-%d_%H%M%S")
                    + os.path.splitext(file)[1]
                )

            # when there is no metadata, move to single folder
            except organize.NoDatetimeFound:
                print("File", file_location, "appears to have no metadata.")

            # move file to new location and name
            if os.path.isfile(file_location) and not os.path.isfile(folder + file_name):
                os.rename(file_location, folder + file_name)
            else:
                print(
                    "Skipping file",
                    file_name,
                    ": it already exists in the target folder.",
                )


if __name__ == "__main__":
    main(sys.argv)
