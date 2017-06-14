from eeg.settings import BASE_DIR
import random
import string


class Loader(object):

    @staticmethod
    def file_dir():
        return '%s/algos/files/' % BASE_DIR

    @staticmethod
    def name_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

    def __init(self):
        self._file_name = ''

    @staticmethod
    def handle_loaded(f, name='', extension='.xlsx'):
        if name is '':
            name = Loader.name_generator()

        full_name = Loader.file_dir() + name + extension
        # raise Exception(full_name)
        with open(full_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return full_name
