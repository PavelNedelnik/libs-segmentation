import numpy as np
import h5py
from typing import Tuple, Optional
from pathlib import Path


def load_h5_dataset(dataset_path: Path) -> Tuple[np.array, Optional[np.array], np.array, list]:
    for file_path in dataset_path.glob('**/*.h5'):
        try:
            f = h5py.File(file_path, "r")
            f = f[list(f.keys())[0]]
            f = f[list(f.keys())[0]]
            f = f['libs']
            print('    Loading dimensions...', end='', flush=True)
            dim = [max(f['metadata']['X']) + 1, max(f['metadata']['Y']) + 1]
            print(' Done!', flush=True)

            print('    Loading spectra...', end='', flush=True)
            X = f['data'][()]
            print(' Done!', flush=True)

            print('    Loading wavelengths...', end='', flush=True)
            wavelengths = np.array(f['calibration'])
            print(' Done!', flush=True)

            print('    Reshaping spectra...', end='', flush=True)
            X = np.reshape(X, dim + [-1])
            X[::2, :] = X[::2, ::-1]
            print(' Done!', flush=True)

            print('    Loading true labels...', end='', flush=True)
            y = None  # TODO
            print(' Done!', flush=True)

            return X, y, wavelengths, dim
        except Exception as e:
            print('\n[WARNING] Failed to load file {} with error message: {}. Skipping!'.format(file_path, e), flush=True)
            continue
    raise RuntimeError('Failed to load! No valid file found!')