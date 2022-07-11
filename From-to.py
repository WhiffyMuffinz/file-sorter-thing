# this one is different because it will have a source folder and a destination folder
# instead of everything in one folder
# Whiffy
# 6/4/21

import os
from shutil import move
from tqdm import tqdm


# commonly used strings
RED_SAV = "redditsave.com"
CONFIG_PATH = r"~/.config/file-sorter-thing/"
CONFIRM_NAME = r"confirm-file-types.conf"
PATHS_NAME = r"paths.conf"

# list of file types that might need confirmation before deletion
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


def main():

    (from_folder, to_folder, confirm_file_types) = config()

    sort(from_folder, to_folder, confirm_file_types)


def config():
    """this function will be used to configure the program"""
    """first check ~/.config/file-sorter-thing/paths.conf for the location of the source and destination folders"""
    """if the file doesn't exist, prompt the user to create it"""
    """then look for a file in the same folder called `confirm-file-types` and add the file types to the list CONFIRM_FILE_TYPES"""

    paths = config_paths()

    confirm_file_types = config_types()
    out: tuple(str, str, list[str]) = (paths[0], paths[1], confirm_file_types)
    return out


def config_paths():
    from_folder, to_folder = "", ""
    # check if the file exists
    if os.path.exists(os.path.expanduser(CONFIG_PATH + PATHS_NAME)):
        # if it does, read the file
        with open(os.path.expanduser(CONFIG_PATH + PATHS_NAME), "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("source"):
                    from_folder = line.split("=")[1].strip()
                    if not os.path.exists(from_folder):
                        print(
                            "There was an error with the source path. Please check the file."
                        )
                        exit()
                if line.startswith("destination"):
                    to_folder = line.split("=")[1].strip()
                    if not os.path.exists(to_folder):
                        print(
                            "There was an error with the destination path. Please check the file."
                        )
                        exit()
    else:
        # if it doesn't, create it and prompt the user to fill it out manualy
        create_path_config()

    out = (from_folder, to_folder)
    return out


def create_path_config():
    os.makedirs(os.path.expanduser(CONFIG_PATH))
    with open(os.path.expanduser(CONFIG_PATH + PATHS_NAME), "w") as f:
        f.write(
            "# this file is used to configure the program\n"
            + "# absolute paths are recommended\n"
            + "# if using Windows, remember to use double backslashes\n"
            + "source="
            + "\n"
            + "destination="
            + "\n"
        )
        print(
            "This program requires configuration of source and destination paths. A configuration file has been created at {}, please look at it".format(
                os.path.expanduser(CONFIG_PATH + PATHS_NAME)
            )
        )
        exit()


def config_types() -> list[str]:
    out = []
    # check if the file exists
    if os.path.exists(os.path.expanduser(CONFIG_PATH + CONFIRM_NAME)):
        # if it does, read the file
        with open(os.path.expanduser(CONFIG_PATH + CONFIRM_NAME), "r") as f:
            lines = f.readlines()
            for line in lines:
                out.append(line.strip())
    else:
        # if it doesn't, create it and add the baked in file types to the list
        with open(os.path.expanduser(CONFIG_PATH + CONFIRM_NAME), "w") as f:

            for ext in CONFIRM_FILE_TYPES:
                f.write(ext + "\n")

            # inform the user that the file has been created, and that they should add the file types to the list
            print(
                "a file for confirming file types has been created in the config folder."
            )
            print(
                "please add the file types you want to be prompted for to the list in the file."
            )
    return out


# main sorting function.
def sort(from_folder: str, to_folder: str, confirm_file_types: list[str]):
    list_ = os.listdir(from_folder)

    for file_ in tqdm(list_):
        name, ext = os.path.splitext(file_)
        print(name, ext)
        ext = ext[1:]
        print(ext)

        if ext.lower() in confirm_file_types:
            confirmations(file_, ext, from_folder, to_folder)
            continue

        if name.split("_")[0] == RED_SAV:
            reddistave_remove(file_, ext, from_folder, to_folder)
            continue

        if os.path.exists(to_folder + "/" + ext):
            move(from_folder + "/" + file_, to_folder + "/" + ext + "/" + file_)
        else:
            os.makedirs(to_folder + "/" + ext)
            move(from_folder + "/" + file_, to_folder + "/" + ext + "/" + file_)


# prompts users if they tould like to delete particular file types
def confirmations(file, ext: str, from_folder: str, to_folder: str):

    print(
        f"\n{file} could be an unneeded file. Would you like to move it to the recycle bin?"
    )

    if input("y/[n] ") == "y":
        os.remove(from_folder + "/" + file)
        print("Sent to trash")
    else:
        print("not sent to trash")
        if os.path.exists(to_folder + "/" + ext):
            move(from_folder + "/" + file, to_folder + "/" + ext + "/" + file)
        else:
            os.makedirs(to_folder + "/" + ext)
            move(from_folder + "/" + file, to_folder + "/" + ext + "/" + file)


# I save lots of videos from reddit, and the service I use adds its name to the saved file, so I remove it
def reddistave_remove(file, ext: str, from_folder: str, to_folder: str):

    old = os.path.basename(file)
    new = old.replace("redditsave.com", "")
    os.rename(from_folder + "/" + old, from_folder + "/" + new)
    move(from_folder + "/" + new, to_folder + "/" + ext + "/" + new)


if __name__ == "__main__":
    main()
