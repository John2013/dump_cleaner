import argparse
import os
import shutil
from operator import attrgetter


class File:
    __slots__ = ('file_path', 'size', 'created_at')

    def __init__(self, file_path, size, created_at):
        self.file_path = file_path
        self.size = size
        self.created_at = created_at

    def delete(self):
        os.remove(self.file_path)


class DumpCleaner:
    def __init__(self, folder, keep_files_count=2, keep_space=2):
        self.folder = folder
        self.keep_files_count = keep_files_count
        self.keep_space = keep_space

        os.chdir(folder)
        self.files = []
        self.free_space = None
        self.get_free_space()

        self.get_files()
        self.files_size = max(*self.files[-1:-2:-1]).size

    def get_free_space(self):
        self.free_space = shutil.disk_usage(self.folder).free

    def clean(self):
        while self.free_space < self.files_size * self.keep_space and (
                len(self.files) > self.keep_files_count):
            self.files.pop(0).delete()
            self.get_free_space()

    def get_files(self):
        for filename in os.listdir("."):
            file_stat = os.stat(filename)
            self.files.append(
                File(filename, file_stat.st_size, file_stat.st_ctime))
        self.files.sort(key=attrgetter('created_at'))


parser = argparse.ArgumentParser(description='Delete old files.')
parser.add_argument(
    '--folder', '-d', type=str, required=False, default='.',
    help='Folder from which old files will be deleted')
parser.add_argument(
    '--keep_files_count', '-f', type=int, required=False, default=1,
    help='How many files will not be deleted')
parser.add_argument(
    '--keep_space', '-s', type=int, required=False, default=2, help=(
        'Files will be deleted until there is space for that number of recent '
        'files'))

if __name__ == '__main__':
    args = parser.parse_args()
    cleaner = DumpCleaner(args.folder, args.keep_files_count, args.keep_space)
    cleaner.clean()
