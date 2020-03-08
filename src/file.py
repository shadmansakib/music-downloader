import os


def create_dir(dir_name, exists_ok=True):
    os.makedirs(os.path.join(dir_name), exist_ok=exists_ok)


def write_binary_file(filepath, data, verbose=False):
    with open(filepath, 'wb') as f:
        if verbose:
            print('Writing file: {}'.format(filepath))
        for chunk in data.iter_content(100000):
            f.write(chunk)
            if verbose:
                print('...')
        if verbose:
            print('File written: {}'.format(filepath))
