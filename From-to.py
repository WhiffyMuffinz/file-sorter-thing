# this one is different because it will have a source folder and a destination folder
# instead of everything in one folder
# Whiffy
# 6/4/21

import os
from shutil import move
from tqdm import tqdm

# these will be the Path of the source folder and the destination folder
FROM_FOLDER = r"C:/Users/Skippy/Downloads"  # the "r" in front of the sring means raw, it lets you put backslashes in the string without the next character being escaped
TO_FOLDER = r"D:/Archive/Random Files"


# commonly used strings
RED_SAV = "redditsave.com"
CONFIRM_LOCATION = r"~/.config/file-sort-thing/confirm-file-types.conf"
PATHS_LOCATION = r"~/.config/file-sort-thing/paths.conf"

# list of file types that might need confirmation
CONFIRM_FILE_TYPES = [
    "exe",
    "msi",
    "jar",
    "jpg~",
    "png~",
    "apk",
    "xapk",
    "appinstaller",
]


# list of files that might need confirmation
NEEDS_CONFIRMATION = []  # leave this list empty

# list of videos whose name starts with redditsave
REDDITSAVE_VIDEOS = []  # leave this list empty


def config():
    """this function will be used to configure the program"""
    """first check ~/.config/file-sort-thing/paths.conf for the location of the source and destination folders"""
    """if the file doesn't exist, prompt the user to create it"""
    """then look for a file in the same folder called `confirm-file-types` and add the file types to the list CONFIRM_FILE_TYPES"""

    conf_paths()
    conf_types()


def conf_paths():
    # check if the file exists
    if os.path.exists(os.path.expanduser(PATHS_LOCATION)):
        # if it does, read the file
        with open(os.path.expanduser(PATHS_LOCATION), "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("source"):
                    FROM_FOLDER = line.split("=")[1].strip()
                    if not os.path.exists(FROM_FOLDER):
                        print(
                            "There was an error with the source path. Please check the file."
                        )
                if line.startswith("destination"):
                    TO_FOLDER = line.split("=")[1].strip()
                    if not os.path.exists(TO_FOLDER):
                        print(
                            "There was an error with the destination path. Please check the file."
                        )
    else:
        # if it doesn't, create it and prompt the user to fill it out manualy
        with open(os.path.expanduser(PATHS_LOCATION), "w") as f:
            f.write(
                "# this file is used to configure the program\n"
                + "# absolute paths are recommended\n"
                + "# if using Windows, remember to use double backslashes\n"
                + "source="
                + "\n"
                + "destination="
                + "\n"
            )


def conf_types():
    # check if the file exists
    if os.path.exists(os.path.expanduser(CONFIRM_LOCATION)):
        # if it does, read the file
        with open(os.path.expanduser(CONFIRM_LOCATION), "r") as f:
            lines = f.readlines()
            for line in lines:
                CONFIRM_FILE_TYPES.append(line.strip())
    else:
        # if it doesn't, create it and add the baked in file types to the list
        with open(os.path.expanduser(CONFIRM_LOCATION), "w") as f:

            for ext in CONFIRM_FILE_TYPES:
                f.write(ext + "\n")

            # inform the user that the file has been created, and that they should add the file types to the list
            print(
                "a file for confirming file types has been created in the config folder."
            )
            print(
                "please add the file types you want to be prompted for to the list in the file."
            )


def main():
    config()
    sort()


# sequential search
def seq_search(to_find, to_search):
    for i in range(len(to_search)):
        tmp = to_search[i]

        if to_find == tmp:
            return i
    return -1


# main sorting function.
def sort():
    list_ = os.listdir(FROM_FOLDER)

    for file_ in tqdm(list_):
        name, ext = os.path.splitext(file_)
        ext = ext[1:]

        if seq_search(ext.lower(), CONFIRM_FILE_TYPES) != -1:
            confirmations(file_, ext)
            continue

        if name.split("_")[0] == RED_SAV:
            reddistave_remove(file_, ext)
            continue

        if os.path.exists(TO_FOLDER + "/" + ext):
            move(FROM_FOLDER + "/" + file_, TO_FOLDER + "/" + ext + "/" + file_)
        else:
            os.makedirs(TO_FOLDER + "/" + ext)
            move(FROM_FOLDER + "/" + file_, TO_FOLDER + "/" + ext + "/" + file_)


# prompts users if they tould like to delete particular file types
def confirmations(file, ext: str):

    print(
        f"\n{file} could be a temp or an installation file. Would you like to move it to the recycle bin?"
    )

    if input("y/[n] ") == "y":
        os.remove(FROM_FOLDER + "/" + file)
        print("Sent to trash")
    else:
        print("not sent to trash")
        if os.path.exists(TO_FOLDER + "/" + ext):
            move(FROM_FOLDER + "/" + file, TO_FOLDER + "/" + ext + "/" + file)
        else:
            os.makedirs(TO_FOLDER + "/" + ext)
            move(FROM_FOLDER + "/" + file, TO_FOLDER + "/" + ext + "/" + file)


# I save lots of videos from reddit, and the service I use adds its name to the saved file, so I remove it
def reddistave_remove(file, ext: str):

    old = os.path.basename(file)
    new = old.replace("redditsave.com", "")
    os.rename(FROM_FOLDER + "/" + old, FROM_FOLDER + "/" + new)
    move(FROM_FOLDER + "/" + new, TO_FOLDER + "/" + ext + "/" + new)


if __name__ == "__main__":
    main()
