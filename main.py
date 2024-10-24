#MIT License

#Copyright (c) 2024 John

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# SHOUTOUT Beyoncé

import os
import argparse
import time
import sys
import hashlib
from send2trash import send2trash

#GLOBAL VARIABLES
verbose=True

##INTRO
print("File manager able to check files for duplicate files and delete them")
print("""DISCLAIMER!!!
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    SOURCE CODE: https://github.com/N-John/File-Cleanup.git
    COPYRIGHT: Copyright (c) 2024 John
    LAST MODIFIIED: 23/10/2024 
      """)


class bcolors:
    """Add Colour for the output"""
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printv(string:str):
    """Setup to enable quiet mode"""
    if verbose:
        print(string)


def convert_size(size_bytes):
    """Convert Bytes to readable Formats"""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int((len(bin(size_bytes)) - 2) / 10)  # Find index for unit
    p = 1024 ** i
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def lpPrefix(filePath):
    if os.name == 'nt' and len(filePath) >= 260:
        return '\\\\?\\' + os.path.abspath(filePath)
    return filePath

def summary(TotalFilesCnt,WalkCount,DupCount,execution_time,deleted=False,SizeChange="",FilesDeleted=0,prevDirSize="0",currentDirSize="0"):
    length=37
   
    print("+"+"-"*(length-2) +"+")
    print(f"| Time taken: {bcolors.BOLD}{execution_time:.2f}{bcolors.ENDC} seconds",end="")
    sys.stdout.write(f"\033[{length}G|\n")
    print(f"| Total Walks: {bcolors.BOLD}{WalkCount}{bcolors.ENDC}",end="")
    sys.stdout.write(f"\033[{length}G|\n")
    print(f"| Total Files checked: {bcolors.BOLD}{TotalFilesCnt}{bcolors.ENDC}",end="")
    sys.stdout.write(f"\033[{length}G|\n")
    print(f"| Total Duplicates Found: {bcolors.FAIL}{bcolors.BOLD}{DupCount}{bcolors.ENDC}",end="")
    sys.stdout.write(f"\033[{length}G|\n")
    if deleted:
        print(f"| Files Deleted: {bcolors.FAIL}{bcolors.BOLD}{FilesDeleted}{bcolors.ENDC}",end="")
        sys.stdout.write(f"\033[{length}G|\n")
        print(f"| Previous Directory Size: {bcolors.FAIL}{bcolors.BOLD}{prevDirSize}{bcolors.ENDC}",end="")
        sys.stdout.write(f"\033[{length}G|\n")
        print(f"| CurrentDirectory Size: {bcolors.FAIL}{bcolors.BOLD}{currentDirSize}{bcolors.ENDC}",end="")
        sys.stdout.write(f"\033[{length}G|\n")
        print(f"| File Change Size: {bcolors.FAIL}{bcolors.BOLD}{SizeChange}{bcolors.ENDC}",end="")
        sys.stdout.write(f"\033[{length}G|\n")

    print("+"+"-"*(length-2)+"+")

def deleteEmptyFiles(root_directory):
    emptyFile_map = {}
    emptyFileCount=0
    for dirpath, dirnames, filenames in os.walk(root_directory):
       
        # Check if file is empty
        for filename in filenames:
            filePath=os.path.join(dirpath, filename)
            pathLeninit=len(filePath)
            filePath = lpPrefix(filePath)
            pathLen=len(filePath)
            fileSize=os.path.getsize(filePath)

            if fileSize ==0:
                emptyFile_map[filename] = filePath
                emptyFileCount=emptyFileCount+1
                #print(filename)

    # Print results
    print(f"The following {bcolors.BOLD}{emptyFileCount}{bcolors.ENDC} files are empty:")
    emptyCount=0
    for name, fpath in emptyFile_map.items():
        emptyCount=emptyCount+1
        print(f"{emptyCount} Name: {bcolors.FAIL}{bcolors.BOLD}{name}{bcolors.ENDC} is empty ")
        file_size = convert_size(os.path.getsize(fpath))
        print(f"  {fpath} [{file_size}]")

def hsFunct(file_path):
    sha256_hash = hashlib.sha256()
    
    with open(file_path, "rb") as f:
        # Read and update hash in chunks
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()

def similarFiles(root_directory,deleteEmpty=False,deleteSimilar=False,permanent=False):
    """Function to comb and look for similar files"""
    print(f" {bcolors.HEADER}Checking for duplicated files {bcolors.ENDC}")

    startTime=time.time() #get start time
    name_map = {}
    filesChecked=0
    WalkCount=0
    TotaldupFilesCount=0
    startFileSize=os.path.getsize(root_directory)
    filesDeletedCnt=0

    for dirpath, dirnames, filenames in os.walk(root_directory):
        WalkCount=WalkCount+1

        for filename in filenames:
            filesChecked=filesChecked+1
            if filename not in name_map:
                name_map[filename] = [os.path.join(dirpath, filename)]
            else:
                name_map[filename].append(os.path.join(dirpath, filename))

    dupCount=0
    for name, paths in name_map.items():
        filesHash={}
        if len(paths) > 1:
            hashCount=0
            hashList=[]
            for fpath in paths:                
                Hsh=hsFunct(fpath)
                filesHash[hashCount]={}
                filesHash[hashCount]["FileHash"]=Hsh
                filesHash[hashCount]["filePath"]=fpath
                filesHash[hashCount]["similarity"]=[]
                hashList.append(Hsh)
                hashCount=hashCount+1

            similarhash=[]
            pathCount=0
            for checkHash in hashList:
                appearance=0
                for val in range(len(hashList)):
                    if checkHash == hashList[val]:
                        appearance=appearance+1
                        pathCount=pathCount+1
                
                if appearance>1:
                    similarhash.append(checkHash)

                while 1:
                    hashList.remove(checkHash)
                    if not checkHash in hashList:
                        break

            if len(similarhash)>0:
                dupCount=dupCount+1
                print(f"{dupCount} Name: {bcolors.FAIL}{bcolors.BOLD}{name}{bcolors.ENDC} has duplicate names in the following variation(s):")

                for currentHash in similarhash:
                    printv(f"Hash_id {bcolors.UNDERLINE}{currentHash}{bcolors.ENDC}")
                    dupFilesCount=0
                    for id,hashings in filesHash.items():
                        if filesHash[id]["FileHash"] == currentHash:
                            
                            if dupFilesCount>=1 and deleteSimilar==True: 
                                filePath=filesHash[id]["filePath"]
                                try:
                                    printv(f"    {bcolors.BOLD}{filesHash[id]["filePath"]}{bcolors.ENDC} {convert_size(os.path.getsize(filesHash[id]["filePath"]))}")
                                    
                                    if permanent:                                        
                                        os.remove(filesHash[id]["filePath"])
                                        print(f"{bcolors.OKGREEN}[DELETED PERMANENT]{bcolors.ENDC}")
                                        filesDeletedCnt=filesDeletedCnt+1
                                    else:
                                        send2trash(filesHash[id]["filePath"])
                                        print(f"{bcolors.OKGREEN}[DELETED]{bcolors.ENDC}")

                                    filesDeletedCnt=filesDeletedCnt+1


                                except FileNotFoundError:
                                    print(f"{bcolors.FAIL}{filesHash[id]["filePath"]} does not exist.{bcolors.ENDC}")
                                except Exception as e:
                                    print(f"{bcolors.FAIL}Error Deleting file at {filesHash[id]["filePath"]}{bcolors.ENDC}: {e}")
                            else:
                                printv(f"    {bcolors.BOLD}{filesHash[id]["filePath"]}{bcolors.ENDC} {convert_size(os.path.getsize(filesHash[id]["filePath"]))}")
                                print(f"{bcolors.OKGREEN}[SAVED]{bcolors.ENDC}")

                            dupFilesCount=dupFilesCount+1
                            TotaldupFilesCount=TotaldupFilesCount+1
                    
                    

                printv("")
    
    EndFileSize=os.path.getsize(root_directory)
    endTime=time.time() 
    execution_time = endTime - startTime

    if deleteSimilar or deleteEmpty:
        deleted=True
        fc=EndFileSize-startFileSize
        Schange=convert_size(fc)


    summary(TotalFilesCnt=filesChecked,WalkCount=WalkCount,DupCount=TotaldupFilesCount,execution_time=execution_time,deleted=deleted,FilesDeleted=filesDeletedCnt,SizeChange=Schange,
    prevDirSize=convert_size(startFileSize),currentDirSize=convert_size(EndFileSize))
    
#MAIN
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for duplicate file and folders.")
    parser.add_argument("directory", nargs='?', default=os.getcwd(),help="The directory to search in")
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed output")
    #parser.add_argument("--empty", action="store_true", help="Only print empty files")
    #parser.add_argument("--deleteEmpty", action="store_true", help="Deletes Empty Files")
    parser.add_argument("--Permanent", action="store_true", help="Deletes Files Permanently")
    parser.add_argument("--deleteCopies", action="store_true", help="Deletes Copy Files")

    args = parser.parse_args()
    
    if args.quiet:
        verbose=False
    similarFiles(args.directory,deleteSimilar=args.deleteCopies,permanent=args.Permanent)
