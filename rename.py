import os
import sys
import organize
import filecmp


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

    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if (
                file.endswith(".jpg")
                or file.endswith(".JPG")
                or file.endswith(".mp4")
                or file.endswith(".MP4")
                or file.endswith(".3gp")
            ):

                file_name = file
                file_location = os.path.join(subdir, file_name)

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
                    print(
                        "File", file_location, "appears to have no metadata. Skipping!"
                    )

                copy_number = 1
                done = False
                while not done:
                    # if the new name and the old one are the same
                    if os.path.isfile(folder + file_name):
                        # test if the same file
                        if filecmp.cmp(
                            file_location,
                            os.path.join(subdir, file_name),
                            shallow=False,
                        ):
                            break
                        # if different files with same name add number
                        else:
                            if copy_number == 1:
                                file_name = (
                                    os.path.splitext(file_name)[0]
                                    + "_"
                                    + str(copy_number)
                                    + os.path.splitext(file_name)[1]
                                )
                            else:
                                file_name = file_name.replace(
                                    "_"
                                    + str(copy_number - 1)
                                    + os.path.splitext(file_name)[1],
                                    "_"
                                    + str(copy_number)
                                    + os.path.splitext(file_name)[1],
                                )
                            copy_number = copy_number + 1
                    else:
                        # move file to new location and name
                        if os.path.isfile(file_location) and not os.path.isfile(
                            os.path.join(subdir, file_name)
                        ):
                            os.rename(file_location, os.path.join(subdir, file_name))
                        done = True


if __name__ == "__main__":
    main(sys.argv)
