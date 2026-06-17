import logging
from pathlib import Path


def write_data_to_file(filename, header, data):
    """Write a header and iterable of data lines to a text file."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with path.open('w') as f:
            f.write(header)
            for line in data:
                f.write(line)
        logging.info('Data successfully written to %s', path)
    except IOError as e:
        logging.error('Failed to write to file %s: %s', path, e)
        raise RuntimeError(f'Failed to write to file {path}') from e
