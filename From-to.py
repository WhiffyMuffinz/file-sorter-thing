# this one is different because it will have a source folder and a destination folder
# instead of everything in one folder
# Whiffy
# 6/4/21

import os
from shutil import move

# these will be the Path of the source folder and the destination folder
FROM_FOLDER = r"C:/Users/Whiffy/Downloads"  # the "r" in front of the sring means raw, it lets you put backslashes in the string without the next character being escaped
TO_FOLDER = r"D:/Archive/Random Files"
BEAT_SABER_SWORD_LOCATION = r""


# list of file types that might need confirmation
CONFIRM_FILE_TYPES = ["exe", "msi", "jar", "jpg~", "png~", "apk", "xapk"]


# list of files that might need confirmation
NEEDS_CONFIRMATION = []  # leave this list empty

# list of videos whose name starts with redditsave
REDDITSAVE_VIDEOS = []  # leave this list empty


def main():
    sort()
    redditsave_remove()
    confirmations()
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
    # make a an organized list of all the files in the folder
    list_ = os.listdir(FROM_FOLDER)
    print("FROM: {}".format(FROM_FOLDER))
    print("TO: {}".format(TO_FOLDER))

    for file_ in list_:
        # split the name of the file at the period
        name, ext = os.path.splitext(file_)

        # idk wtf this does
        ext = ext[1:]

        # if ext == "" or seq_search(ext, EXCLUDE) != -1:
        #    continue

        if seq_search(ext, CONFIRM_FILE_TYPES) != -1:
            NEEDS_CONFIRMATION.append(file_)
            continue

        if name.split("_")[0] == "redditsave.com":
            REDDITSAVE_VIDEOS.append(file_)
            continue

        if ext == "saber":
            move(FROM_FOLDER + "/" + file_, BEAT_SABER_SWORD_LOCATION + "/" + file_)
            continue

        if os.path.exists(TO_FOLDER + "/" + ext):
            move(FROM_FOLDER + "/" + file_, TO_FOLDER + "/" + ext + "/" + file_)
        else:
            os.makedirs(TO_FOLDER + "/" + ext)
            move(FROM_FOLDER + "/" + file_, TO_FOLDER + "/" + ext + "/" + file_)


# prompts users if they tould like to delete particular file types
def confirmations():
    for file_ in NEEDS_CONFIRMATION:
        print(
            f"\n{file_} could be a temp or an installation file. Would you like to move it to the recycle bin?"
        )

        _name, ext = os.path.splitext(file_)

        try:
            if input("y/[n] ") == "y":
                os.remove(FROM_FOLDER + "/" + file_)
                print("Sent to trash")
            else:
                print("not sent to trash")
                move(FROM_FOLDER + "/" + file_, TO_FOLDER + "/" + ext + "/" + file_)
        except:
            print(r"There was a problem or something, idk ¯\_(ツ)_/¯")
            # println(e)
            continue


def handle_name_conflict(file_from: str, file_to: str):
    """handles a naming conflict between two files
    Params: 
    file_from: path of the file in source folder 
    file_to: path of the file in destination folder"""


# I save lots of videos from reddit, and the service I use adds its name to the saved file, so I remove it
def redditsave_remove():
    for i in REDDITSAVE_VIDEOS:
        name, ext = os.path.splitext(i)
        old = os.path.basename(i)
        new = old.replace("redditsave.com", "")
        os.rename(FROM_FOLDER + "/" + old, FROM_FOLDER + "/" + new)


if __name__ == "__main__":
    main()
