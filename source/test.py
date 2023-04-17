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