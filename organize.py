import os
import sys
import exifhandling


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
            or file.endswith(".NEF")
        ):
            file_name = file
            file_location = folder + file_name

            # extract the day and time a file was created
            try:
                if file.endswith(".jpg") or file.endswith(".JPG"):
                    creation_date = exifhandling.extract_from_image(file_location)
                else:
                    creation_date = exifhandling.extract_from_video(file_location)

                # rename if there is metadata
                file_name = (
                    creation_date.strftime("%Y-%m-%d_%H%M%S")
                    + os.path.splitext(file)[1]
                )

                # new folders if there is metadata
                top_new_path = str(creation_date.year) + "/"
                if not os.path.exists(top_new_path):
                    os.mkdir(top_new_path)
                new_path = top_new_path + str(creation_date.month).zfill(2) + "/"
                if not os.path.exists(new_path):
                    os.mkdir(new_path)

            # when there is no metadata, move to single folder
            except exifhandling.NoDatetimeFound:
                print("File", file_location, "appears to have no metadata.")
                new_path = "no_metadata/"
                if not os.path.exists(new_path):
                    os.mkdir(new_path)

            # move file to new location and name
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
