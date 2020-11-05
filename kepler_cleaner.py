import glob
import os

kepler_models_path = os.environ['KEPLER_MODELS']


# ==================================================
#                   Clean
# ==================================================
def clean_all_models(model_set, batch_basename=None):
    """Remove all but first and last dumpfiles in a model_set
    """
    model_list = get_full_model_list(model_set=model_set,
                                     batch_basename=batch_basename)

    print(20*'=')
    clean_all_logs(model_set=model_set)
    print(20*'=')

    for model_path in model_list:
        print(f'Cleaning: {model_path}')
        clean_model_dumpfiles(model_path=model_path)
        clean_model_ascii(model_path=model_path)

    print(f'Finished cleaning {len(model_list)} models')


def clean_model_dumpfiles(model_path):
    """Remove all but first and last dumpfiles in a model
    """
    dumpfile_paths = get_dumpfile_list(model_path=model_path)
    dumpfiles = get_sorted_dumpfiles(dumpfile_paths)

    model = model_path.split(sep='/')[-1]

    for dump in dumpfiles[1:-1]:
        path = os.path.join(model_path, f'{model}#{dump}')
        os.remove(path)


def clean_model_ascii(model_path):
    """Remove ascii logfiles
    """
    ascii_paths = get_all_ascii(model_path=model_path)

    for asci in ascii_paths:
        os.remove(asci)


def clean_all_logs(model_set, batch_basename=None):
    """Delete all log dirs
    """
    logpaths = get_all_logpaths(model_set=model_set, batch_basename=batch_basename)

    for log in logpaths:
        path = os.path.join(log, '*')
        file_list = glob.glob(path)
        print(f'Removing: {log}')

        for f in file_list:
            os.remove(f)
        os.rmdir(log)


# ==================================================
#                   paths/lists
# ==================================================
def get_all_logpaths(model_set, batch_basename=None):
    """Return list of paths to all log dirs
    """
    logpaths = []
    batch_list = get_batch_list(model_set, batch_basename=batch_basename)

    for batch_path in batch_list:
        path = os.path.join(batch_path, 'logs')
        logpaths += glob.glob(path)

    return logpaths


def get_all_ascii(model_path, basename='xrb'):
    """Return list of paths to ascii logfiles
    """
    path = os.path.join(model_path, f'{basename}*_*0')
    return glob.glob(path)


def get_batch_list(model_set, batch_basename=None):
    """Return list of paths to model batch dirs
    """
    batch_basename = check_basename(model_set, batch_basename=batch_basename)
    path = os.path.join(kepler_models_path, model_set, f'{batch_basename}_*')
    return glob.glob(path)


def get_full_model_list(model_set, basename='xrb', batch_basename=None):
    """Return full list of model paths in a model_set
    """
    model_list = []
    batch_list = get_batch_list(model_set=model_set, batch_basename=batch_basename)

    for batch_path in batch_list:
        model_list += get_model_list(batch_path=batch_path, basename=basename)

    return model_list


def get_model_list(batch_path, basename='xrb'):
    """Return list of model paths in a batch
    """
    path = os.path.join(batch_path, f'{basename}*')
    return glob.glob(path)


def get_dumpfile_list(model_path, basename='xrb'):
    """Return list of filepaths to dumpfiles
    """
    path = os.path.join(model_path, f'{basename}*#*')
    return glob.glob(path)


def get_sorted_dumpfiles(dumpfile_list):
    """Return list of sorted dumpfile numbers
    """
    dumps = []

    for path in dumpfile_list:
        n = path.split(sep='#')[-1]
        dumps += [int(n)]

    dumps.sort()
    return dumps


def check_basename(model_set, batch_basename):
    if batch_basename is None:
        batch_basename = model_set

    return batch_basename
