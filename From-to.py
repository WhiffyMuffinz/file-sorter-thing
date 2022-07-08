# this one is different because it will have a source folder and a destination folder
# instead of everything in one folder
# Whiffy
# 6/4/21

import os
from shutil import move
from tqdm import tqdm

# these will be the Path of the source folder and the destination folder
FROM_FOLDER = r"C:/Users/Whiffy/Downloads"  # the "r" in front of the sring means raw, it lets you put backslashes in the string without the next character being escaped
TO_FOLDER = r"D:/Archive/Random Files"
BEAT_SABER_SWORD_LOCATION = r""
RED_SAV = "redditsave.com"

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


def main():
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
