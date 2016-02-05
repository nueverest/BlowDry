# python 2
from builtins import str
# builtin
from unittest import TestCase
from os import path, getcwd, remove
# custom
from blowdrycss.filehandler import GenericFile

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestGenericFile(TestCase):
    def test_write_valid(self):
        sample_markdown = '# Sample Title\nThis is a paragraph.\n'
        expected_string = sample_markdown

        cwd = getcwd()
        if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
            generic_directory = path.join(cwd, 'test_generic')
        else:                                                       # Run unittest cmd from the root directory.
            generic_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_generic')

        file_name = 'blowdry'
        extensions = ['.md', '.rst', '.html', '.txt', ]

        for extension in extensions:
            generic_file = GenericFile(file_directory=generic_directory, file_name=file_name, extension=extension)

            if path.isfile(generic_file.file_path):      # Ensure that file is deleted before testing.
                remove(generic_file.file_path)

            generic_file.write(text=str(sample_markdown))

            with open(generic_file.file_path, 'r') as generic_file:
                file_string = generic_file.read()
            self.assertEqual(file_string, expected_string)

    def test_write_invalid_input(self):
        invalid_inputs = [1239487.234, ['nth', 'rcghtn'], {2, 1, '&^'}, 546, ]

        cwd = getcwd()
        if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
            generic_directory = path.join(cwd, 'test_generic')
        else:                                                       # Run unittest cmd from the root directory.
            generic_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_generic')

        file_name = 'blowdry'
        extension = '.md'

        for invalid_text in invalid_inputs:
            generic_file = GenericFile(file_directory=generic_directory, file_name=file_name, extension=extension)
            self.assertRaises(TypeError, generic_file.write, invalid_text)

    def test_invalid_initialization(self):
        cwd = getcwd()
        if cwd.endswith('unit_tests'):                              # Allows running of pycharm unittest.
            generic_directory = path.join(cwd, 'test_generic')
        else:                                                       # Run unittest cmd from the root directory.
            generic_directory = path.join(cwd, 'blowdrycss', 'unit_tests', 'test_generic')

        file_name = 'blowdry'
        extension = '.md'

        self.assertRaises(ValueError, GenericFile, '', file_name, extension)
        self.assertRaises(ValueError, GenericFile, generic_directory, '', extension)
        self.assertRaises(ValueError, GenericFile, generic_directory, file_name, '')