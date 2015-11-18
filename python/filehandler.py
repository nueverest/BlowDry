from os import path, walk, getcwd, makedirs
from glob import glob
from re import findall
from cssutils import parseString, ser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class FileFinder(object):
    file_types = ('*.html', '*.aspx', '*.master', '*.ascx')

    def __init__(self, project_directory=getcwd(), file_types=file_types):
        if path.isdir(project_directory):
            self.project_directory = project_directory
            self.file_types = file_types
            self.files = []
            print('Project Directory:', project_directory)
            print('\nFile Types:', self.file_types)

            self.set_files()
            print('\nProject Files Found:')
            self.print_collection(self.files)
        else:
            raise NotADirectoryError(project_directory + ' is not a directory.')

    # Takes a list or tuple as input and prints each item.
    @staticmethod
    def print_collection(collection):
        for item in collection:
            print(item)

    # Get all files associated with defined file_types in project directory
    # Reference:
    # stackoverflow.com/questions/954504/how-to-get-files-in-a-directory-including-all-subdirectories#answer-954948
    def set_files(self):
        for directory, _, _ in walk(self.project_directory):
            for file_type in self.file_types:
                self.files.extend(glob(path.join(directory, file_type)))


class FileConverter(object):
    # Converts text files to strings.
    # Ensure the existence of the file_path.
    def __init__(self, file_path=''):
        if path.isfile(file_path):
            self.file_path = file_path
        else:
            raise FileNotFoundError('No file found at: ' + file_path)

    # Convert the file to a string and return it.
    def get_file_as_string(self):
        with open(self.file_path, 'r') as file:
            file_as_string = file.read().replace('\n', '')
        return file_as_string


class CSSFile(object):
    # File name does not include extension.
    # Reference: stackoverflow.com
    # /questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary#answer-14364249
    def __init__(self, file_directory=getcwd(), file_name='blowdry'):
        self.file_directory = file_directory
        self.file_name = file_name
        try:                                        # Python 2.7 Compliant
            makedirs(file_directory)                # Make 'css' directory
        except OSError:
            if not path.isdir(file_directory):      # Verify directory existences
                raise OSError(file_directory + ' is not a directory, and could not be created.')

    # Transform extension to lowercase.
    # Only allow '.', '0-9', and 'a-z' characters.
    def file_path(self, extension=''):
        extension = extension.lower()
        if len(findall(r"([.0-9a-z])", extension)) == len(extension):
            return path.join(self.file_directory, self.file_name + extension)
        else:
            raise ValueError(extension + ' contains invalid characters. Only ".", "0-9", and "a-z" are allowed.')

    # Output a human readable version of the css file in utf-8 format.
    # Note: Overwrites any pre-existing files with the same name.
    def write_css(self, css_text=''):
        parse_string = parseString(css_text)
        ser.prefs.useDefaults()                # Enables Default / Verbose Mode
        with open(self.file_path(extension='.css'), 'w') as css_file:
            css_file.write(parse_string.cssText.decode('utf-8'))

    # Output a minified version of the css file in utf-8 format.
    # Note: Overwrites any pre-existing files with the same name.
    def minify(self, css_text=''):
        parse_string = parseString(css_text)
        ser.prefs.useMinified()                 # Enables Minification
        with open(self.file_path(extension='.min.css'), 'w') as css_file:
            css_file.write(parse_string.cssText.decode('utf-8'))
