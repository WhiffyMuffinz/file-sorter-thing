# this one is different because it will have a source filder and a destination folder 
# instead of everything in one folder
# Daniel B. 
# 6/4/21 

import os
from shutil import move

#these will be the Path of the source folder and the destination folder
FROM_FOLDER = r'C:\Users\Whiffy\Downloads'
TO_FOLDER = r'D:\Random Files'
BEAT_SABER_SWORD_LOCATION = r'D:\Program Files(x86)\SteamLibrary\steamapps\common\Beat Saber\CustomSabers'



#excluded filetypes
EXCLUDE = ['ini', '2', 'lnk', '7z', 'java', 'py', '11103', '1']

#list of file types that might need confirmation
CONFIRM_FILE_TYPES = ['exe', 'msi', 'jar']

#list of files that might need confirmation
NEEDS_CONFIRMATION = []

#list of videos whose name starts with redditsave
REDDITSAVE_VIDEOS = []

def main():
    sort()
    redditsaveRemove()
    confirmations()

def seqSearch(to_find, to_search):
    for i in range(len(to_search)):
        tmp = to_search[i]

        if to_find == tmp:
            return i
    return -1

def sort():
    #make a an organized list of all the files in the folder
    list_ = os.listdir(FROM_FOLDER)
    print('FROM: {}'.format(FROM_FOLDER))
    print('TO: {}'.format(TO_FOLDER))

    for file_ in list_:
        #split the name of the file at the period 
        name, ext = os.path.splitext(file_)

        #idk wtf this does
        ext = ext[1:]

        if ext == '' or seqSearch(ext, EXCLUDE) != -1:
            continue

        if seqSearch(ext, CONFIRM_FILE_TYPES) != -1:
            NEEDS_CONFIRMATION.append(file_)
            continue

        if name.split("_")[0] == "redditsave.com":
            REDDITSAVE_VIDEOS.append(file_)
            continue

        if ext == 'saber':
            move(FROM_FOLDER + '/' + file_, BEAT_SABER_SWORD_LOCATION + '/' + file_)
            continue

        if os.path.exists(TO_FOLDER + '/' + ext):
            move(FROM_FOLDER + '/' + file_, TO_FOLDER + '/' + ext + '/' + file_)
        else:
            os.makedirs(TO_FOLDER + '/' + ext)
            move(FROM_FOLDER + '/' + file_, TO_FOLDER + '/' + ext + '/' + file_)

def confirmations():
    for file_ in NEEDS_CONFIRMATION:
        print('\n' + file_ + ' might be an installation file, would you like to move it to the recycle bin?')
        
        name, ext = os.path.splitext(file_)

        try:
            if input("y/[n] ") == "y":
                os.remove(FROM_FOLDER + '/' + file_)
                print('Sent to trash')
            else:
                print('not sent to trash')
                move(FROM_FOLDER + '/' + file_, TO_FOLDER + '/' + ext + '/' + file_)
        except:
            print(r"There was a problem or something, idk ¯\_(ツ)_/¯")
            continue


def redditsaveRemove():
    for i in REDDITSAVE_VIDEOS:
        name, ext = os.path.splitext(i)
        old = os.path.basename(i)
        new = old.replace("redditsave.com", "")
        new = new.split("-", 1)[0] + ext
        os.rename(FROM_FOLDER + '/' + old, FROM_FOLDER + '/' + new)
        #try:
        #    move(FROM_FOLDER + '/' + new, TO_FOLDER + '/' + ext + '/' + new)
        #except:
        #    print("there was an error when trying to move a \"redditsave\" video. re-execute the program and see what happens")
        sort()

if __name__ == '__main__':
    main()