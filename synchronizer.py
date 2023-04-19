import argparse
import hashlib
import shutil
import time
import os

class SynchronizeFolders:
       
    def __init__(self, source_folder, destination_folder, log_file, interval):
        self.source = source_folder
        self.replica = destination_folder
        self.log = log_file
        self.interval = interval

    def logs(self, message):
        """Logging actions into log file and displaying them into the command line"""
        now = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        with open(self.log, "a") as log_file:
            log_file.write(f'[{now}] - {message} \n')
        print(f'[{now}] - {message}')

    def check_files(self, source_file, replica_file):
        """Checking if content of both files is the same or not"""
        if os.path.isfile(source_file):
            with open(source_file, 'rb') as source_f:
                with open(replica_file, 'rb') as replica_f:
                    if hashlib.md5(source_f.read()).hexdigest() == hashlib.md5(replica_f.read()).hexdigest():
                        return True
                    return False
        return True
    
    def get_all_files(self):
        """Getting all the files/dirs from source and replica folders and appending them to a dictionaries"""
        source_files = {}
        source_dirs = {}

        replica_files = {}
        replica_dirs = {}

        for root, dirs, files in os.walk(self.source, topdown=True):
            for name in files:
                source_files[name] = f'{root}\{name}'
            for name in dirs:
                source_dirs[name] = f'{root}\{name}'

        for root, dirs, files in os.walk(self.replica, topdown=True):
            for name in files:
                replica_files[name] = f'{root}\{name}'
            for name in dirs:
                replica_dirs[name] = f'{root}\{name}'

        return source_files, source_dirs, replica_files, replica_dirs

    def check_main_folders(self):
        """Checking if files and dirs are the same in replica folder and in source folder"""
        source_files, source_dirs, replica_files, replica_dirs = self.get_all_files()

        if len(source_files) != len(replica_files) or len(source_dirs) != len(replica_dirs):
            return False

        for source_dir in source_dirs:
            if not source_dir in replica_dirs:
                return False

        for source_file, source_root in source_files.items():
            if source_file in replica_files:
                if not self.check_files(source_root, replica_files[source_file]):
                    return False
            else:
                return False
        else:
            return True

    def synchronize(self):
        """Updating replica folder if files/dirs are not the same in both folders"""
        source_files, source_dirs, replica_files, replica_dirs = self.get_all_files()

        for source_dir_name, source_dir in source_dirs.items():
            if source_dir_name not in replica_dirs:
                destination_dir = source_dir.split(self.source)
                os.system(f'xcopy \"{source_dir}\" \"{self.replica}{destination_dir[1]}\" /T /E /H /C /I')
                self.logs(f'CREATED "{source_dir_name}" directory')

        for source_filename, source_file in source_files.items():
            if source_filename not in replica_files:
                destination_file = source_file.replace(source_filename, '').split(self.source)
                os.system(f'xcopy \"{source_file}\" \"{self.replica}{destination_file[1]}\" /I /F')
                self.logs(f'CREATED "{source_filename}" file')
            else:
                if self.check_files(source_file, replica_files[source_filename]):
                    pass
                else:
                    destination_file = source_file.replace(source_filename, '').split(self.source)
                    os.remove(replica_files[source_filename])
                    os.system(f'xcopy \"{source_file}\" \"{self.replica}{destination_file[1]}\" /I /F')
                    self.logs(f'UPDATED "{source_filename}" file')
        
        for replica_dir_name, replica_dir in replica_dirs.items():
            if not replica_dir_name in source_dirs:
                shutil.rmtree(replica_dir)
                self.logs(f'REMOVED "{replica_dir_name}" directory')
                return self.synchronize()
        
        for replica_filename, replica_file in replica_files.items():
            if not replica_filename in source_files:
                os.remove(replica_file)
                self.logs(f'REMOVED "{replica_filename}" file')

    #Main loop
    def main(self):
        while True:
            if self.check_main_folders():
                time.sleep(self.interval*60)
                continue
            else:
                self.synchronize()


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('-s', '--source', type=str, help='Url to source folder.')
    args.add_argument('-r', '--replica', type=str, help='Url to replica folder.')
    args.add_argument('-l', '--log', type=str, help='Url to log file.')
    args.add_argument('-i', '--interval', type=int, help='Time of interval (In minutes).')

    arguments = args.parse_args()

    sync = SynchronizeFolders(arguments.source, arguments.replica, arguments.log, arguments.interval)
    sync.main()