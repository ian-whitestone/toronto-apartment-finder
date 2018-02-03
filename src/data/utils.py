import logging
import sys
import yaml


def read_yaml(yaml_file):
    """Load the contents of a yaml file into an object.

    Parameters
    ----------
    yaml_file : str
        Full path of the yaml file.

    Returns
    -------
    data : dict
        Dictionary of yaml_file contents.

    Raises
    ------
        Exception: If the yaml_file cannot be opened.
    """

    try:
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        log.error('Unable to read file %s. Error: %s' % (yaml_file, e))
        raise
