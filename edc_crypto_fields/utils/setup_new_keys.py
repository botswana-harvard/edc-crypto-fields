import os
import sys
from datetime import datetime

from django.conf import settings

from ..classes import KeyGenerator


def setup_new_keys(key_path=None):

    """ Utility to generate all new keys for the project."""
    key_path = key_path or settings.KEY_PATH
    key_generator = KeyGenerator(key_path)
    paths = key_generator.get_key_paths()
    backup_keys(key_path, paths)

    if old_keys_exist(paths):
        print('Failing. Old keys are still in the target folder. Try moving them manually to a backup folder.')
    else:
        print('Creating new keys')
        # an instance of cryptor was created earlier
        del key_generator
        # now have an empty target folder so guaranteed to
        # not load old keys
        key_generator = KeyGenerator(key_path)
        key_generator.create_new_keys()
        sys.stdout.flush()

        missing_key = False
        for path in paths:
            oldpath = os.path.join(os.path.realpath('.'), path)
            if not os.path.exists(oldpath):
                missing_key = True
                break
        if missing_key:
            print(
                'Failed. Not all keys were created. Delete all keys '
                'from the target folder and try again. Stopped on {0}.'.format(path))
        else:
            print('Complete. All keys were created successfully.')


def backup_keys(key_path, paths):
    backup_path = create_backup_path(key_path)
    for path in paths:
        try:
            oldpath = os.path.join(os.path.realpath('.'), path)
            # newpath has datestring prefix which will be removed once
            # confirmed that ALL keys are new
            newpath = os.path.join(os.path.join(os.path.realpath('.'), backup_path), path.split('/')[-1:][0])
            if os.path.exists(oldpath):
                os.rename(oldpath, newpath)
                print('copied {0}'.format(path))
        except OSError as e:
            print ('Failed to copy {0} to {1}'.format(oldpath, newpath))
            print (e)
            break


def create_backup_path(key_path):
    datestring = datetime.today().strftime('%Y%m%d%H%M%S%f')
    try:
        backup_path = os.path.join(key_path, 'keys_backup_{0}'.format(datestring))
        os.mkdir(backup_path)
        print(backup_path)
    except:
        raise TypeError('Failed to create backup folder')
    return backup_path


def old_keys_exist(paths):
    old_keys_exist = False
    for path in paths:
        oldpath = os.path.join(os.path.realpath('.'), path)
        if os.path.exists(oldpath):
            old_keys_exist = True
            break
    return old_keys_exist
