# this one is different because it will have a source filder and a destination folder
# instead of everything in one folder
# Whiffy
# 6/4/21

import os
from shutil import move

# these will be the Path of the source folder and the destination folder
FROM_FOLDER = r"C:\Users\Whiffy\Downloads"  # the "r" in front of the sring means raw, it lets you put backslashes in the string without the next character being escaped
TO_FOLDER = r"D:\Random Files"
BEAT_SABER_SWORD_LOCATION = (
    r"D:\Program Files(x86)\SteamLibrary\steamapps\common\Beat Saber\CustomSabers"
)


# excluded filetypes
EXCLUDE = ["ini", "2", "lnk", "7z", "java", "py", "11103", "1"]

# list of file types that might need confirmation
CONFIRM_FILE_TYPES = ["exe", "msi", "jar"]

# list of files that might need confirmation
NEEDS_CONFIRMATION = []  # leave this list empty

# list of videos whose name starts with redditsave
REDDITSAVE_VIDEOS = []  # leave this list empty


def main():
    sort()
    redditsave_remove()
    confirmations()


# sequential search
def seq_search(to_find: str, to_search: "list[str]"):
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
    # dest_list = os.listdir(TO_FOLDER)
    print("TO: {}".format(TO_FOLDER))

    for file_ in list_:
        # split the name of the file at the period
        name, ext = os.path.splitext(file_)

        # idk wtf this does
        ext = ext[1:]

        # if name_conflicts(file_, dest_list):
        #    continue

        if ext == "" or seq_search(ext, EXCLUDE) != -1:
            continue

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
            try:
                move(FROM_FOLDER + "/" + file_, TO_FOLDER + "/" + ext + "/" + file_)
            except FileExistsError:
                print(
                    "Rename file {} because it has the same name as another file in the destination".format(
                        FROM_FOLDER + "/" + file_
                    )
                )
                continue
        else:
            os.makedirs(TO_FOLDER + "/" + ext)
            move(FROM_FOLDER + "/" + file_, TO_FOLDER + "/" + ext + "/" + file_)
        sort()


# prompts users if they tould like to delete particular file types
def confirmations():
    for file_ in NEEDS_CONFIRMATION:
        print(
            "\n"
            + file_
            + " might be an installation file, would you like to move it to the recycle bin?"
        )

        name, ext = os.path.splitext(file_)

        try:
            if input("y/[n] ") == "y":
                os.remove(FROM_FOLDER + "/" + file_)
                print("Sent to trash")
            else:
                print("not sent to trash")
                move(FROM_FOLDER + "/" + file_, TO_FOLDER + "/" + ext + "/" + file_)
        except Exception:
            print(r"There was a problem or something, idk ¯\_(ツ)_/¯")
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
        new = new.split("-", 1)[0] + ext
        os.rename(FROM_FOLDER + "/" + old, FROM_FOLDER + "/" + new)
    


if __name__ == "__main__":
    main()
