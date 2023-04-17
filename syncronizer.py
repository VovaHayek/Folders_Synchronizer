import hashlib
import time
import os

class SyncronizeFolders:
       
    def __init__(self, source_folder, destination_folder):
        self.source = source_folder
        self.replica = destination_folder

    def check_files(self, source_file, replica_file):
        if os.path.isfile(source_file):
            with open(source_file, 'rb') as source_f:
                with open(replica_file, 'rb') as replica_f:
                    if hashlib.md5(source_f.read()).hexdigest() == hashlib.md5(replica_f.read()).hexdigest():
                        return True
                    return False
        return True

    def check_main_folders(self):
        source_files = os.listdir(self.source)
        replica_files = os.listdir(self.replica)

        if len(source_files) != len(replica_files):
            return False
        
        for source_file in source_files:
            if source_file in replica_files:
                if not self.check_files(f'{self.source}/{source_file}', f'{self.replica}/{source_file}'):
                    return False
            else:
                return False
        else:
            return True

    #Function for removing/updating/adding files if replica folder doesn't match source folder
    def syncronize(self):
        source_files = os.listdir(self.source)
        replica_files = os.listdir(self.replica)

        #Loop for checking if replica's files match source folder files
        for replica_file in replica_files:
            if replica_file in source_files:
                if self.check_files(f'{self.source}\{replica_file}', f'{self.replica}\{replica_file}'):
                    print('File does exist and same as source file!')
                else:
                    os.remove(f'{self.replica}\{replica_file}')
                    os.system(f'Xcopy \"{self.source}\{replica_file}\" \"{self.replica}\" \T /E /H /C /I')
                    print('File was updated!')
            if replica_file not in source_files:
                os.remove(f'{self.replica}\{replica_file}')
                print('File was deleted!')

        #Loop for checking if source's files match replica folder files (If not, we deleting files/folders from replica folder)
        for source_file in source_files:
            if source_file not in replica_files:
                if os.path.isfile(f'{self.source}\{source_file}'):
                    print(f'xcopy \"{self.source}\{source_file}\" \"{self.replica}\"')
                    os.system(f'xcopy \"{self.source}\{source_file}\" \"{self.replica}\"')
                if os.path.isdir(f'{self.source}\{source_file}'):
                    print(f'xcopy \"{self.source}\{source_file}\" \"{self.replica}\{source_file}\" /T /E /H /C /I')
                    os.system(f'xcopy \"{self.source}\{source_file}\" \"{self.replica}\{source_file}\" /T /E /H /C /I')

    #Main loop
    def main(self):
        while True:
            if self.check_main_folders():
                print("Everything is fine")
                time.sleep(5)
                continue

            self.syncronize()



if __name__ == "__main__":
    source = input("Enter source folder url: ")
    replica = input("Enter replica folder url: ")

    sync = SyncronizeFolders(source, replica)
    sync.main()