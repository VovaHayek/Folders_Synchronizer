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
    
    def get_all_files(self):
        source_files = {}
        source_dirs = {}

        replica_files = {}
        replica_dirs = {}

        for root, dirs, files in os.walk(self.source, topdown=True):
            for name in files:
                print(f'FILE - {root}\{name}')
                source_files[name] = f'{root}\{name}'
            for name in dirs:
                print(f'DIRR - {root}\{name}')
                source_dirs[name] = f'{root}\{name}'

        for root, dirs, files in os.walk(self.replica, topdown=True):
            for name in files:
                replica_files[name] = f'{root}\{name}'
            for name in dirs:
                replica_dirs[name] = f'{root}\{name}'

        return source_files, source_dirs, replica_files, replica_dirs

    def check_main_folders(self):
        source_files, source_dirs, replica_files, replica_dirs = self.get_all_files()

        for source_dir in source_dirs:
            if not source_dir in replica_dirs:
                return False


        for source_file, source_root in source_files.items():
            if source_file in replica_files:
                if not self.check_files(source_root, replica_files[source_file]):
                    print('52')
                    return False
            else:
                print('56')
                return False
        else:
            return True

    #Function for removing/updating/adding files if replica folder doesn't match source folder
    def syncronize(self):
        source_files, source_dirs, replica_files, replica_dirs = self.get_all_files()

        for source_dir_name, source_dir in source_dirs.items():
            if source_dir_name not in replica_dirs:
                destination_dir = source_dir.split(self.source)
                os.system(f'xcopy \"{source_dir}\" \"{self.replica}{destination_dir[1]}\" /T /E /H /C /I')

        for source_filename, source_file in source_files.items():
            if source_filename not in replica_files:
                destination_file = source_file.replace(source_filename, '').split(self.source)
                os.system(f'xcopy \"{source_file}\" \"{self.replica}{destination_file[1]}\" /I /F')
            else:
                if self.check_files(source_file, replica_files[source_filename]):
                    pass
                else:
                    destination_file = source_file.replace(source_filename, '').split(self.source)
                    os.remove(replica_files[source_filename])
                    os.system(f'xcopy \"{source_file}\" \"{self.replica}{destination_file[1]}\" /I /F')
                    print(f'Changed content of - {source_filename}')

    #Main loop
    def main(self):
        while True:
            if self.check_main_folders():
                print("Everything is fine")
                time.sleep(5)
                continue
            else:
                self.syncronize()


if __name__ == "__main__":
    source = input("Enter source folder url: ")
    replica = input("Enter replica folder url: ")

    sync = SyncronizeFolders(source, replica)
    sync.main()