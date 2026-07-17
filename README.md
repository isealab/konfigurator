![Tests](https://github.com/isealab/konfigurator/actions/workflows/test.yml/badge.svg)
![Python versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)

# konfigurator

**konfigurator** is a lightweight Python configuration management utility that allows you to define, override, and instantiate configuration dictionaries and Python classes from simple config files or command-line arguments.

Further, it allows you to instantiate objects from classes using import paths. In this way, *no global registry or any disclosure* of your private code is needed.

The instantiation via import path is inspired by https://github.com/Farama-Foundation/HighwayEnv

## Features

- Load Python-based configuration files as dictionaries.
- Override configuration parameters via command-line.
- Instantiate Python classes from config dictionaries using import paths.
- Save resolved configs to JSON and reload them later.

## Installation
`cd` into repository and run
```bash
pip install .
````

To install in developer mode (with `pre-commit` and `pytest`) run
```bash
pip install -e .[dev]
```

## Usage

1. Load a configuration file

    Your configuration file is a pure python file (e.g., config.py) should define a dictionary named config:
    ```python
    # config.py
    work_dir = "/tmp/my_work_dir"
    class_config_1: {
        "type": "my_module.MyClass",
        "name": "default_name"
    }
    ```
    You will be able to instantiate an object from the configuration `class_config_1` (see ).

    Load this configuration in Python:
    ```python
    from konfigurator import load_config

    config = load_config(config_path="config.py")
    ```

2. Override from command-line and save result

    You can override nested config values via CLI and save the modified config to disk, e.g.:
    ```bash
    python script.py \
    --config config.py \
    --override experiment_dir=/tmp/experiment \
    --override class_config_1.name=overridden_name \
    --override class_config_1.type=5.0
    ```
    Currently, floats, ints, and booleans are converted into their respective type. Strings and other types remain strings.

3. Instantiate classes from config

    Use the `instantiate_class_from_config` to build objects dynamically (IMPORTANT: the value for the key `type` defines the import path):
    ```python
    from konfigurator import instantiate_object_from_config

    class_config_1: {
        "type": "my_module.MyClass",
        "name": "default_name"
    }

    my_obj = instantiate_object_from_config(class_config_1)
    ```

4. Save and reload a resolved config as JSON

    ```python
    from konfigurator import load_config, save_config_to_json, load_config_from_json

    config = load_config(config_path="config.py")
    save_config_to_json(config, "config.json")

    # later, e.g. in a different process
    config = load_config_from_json("config.json")
    ```

## Deployment

Releases are built and published to PyPI manually using [`build`](https://pypi.org/project/build/)
and [`twine`](https://pypi.org/project/twine/), both included in the `dev` extra.

1. Bump the `version` field in [`pyproject.toml`](pyproject.toml) (follow [SemVer](https://semver.org/)).

2. Build the source distribution and wheel:
    ```bash
    python -m build
    ```
    This produces `dist/konfigurator-<version>.tar.gz` and `dist/konfigurator-<version>-py3-none-any.whl`.

3. Sanity-check the built artifacts before uploading:
    ```bash
    twine check dist/*
    ```

4. (Optional but recommended) Upload to [TestPyPI](https://test.pypi.org/) first and verify the
   install works:
    ```bash
    twine upload --repository testpypi dist/*
    pip install --index-url https://test.pypi.org/simple/ konfigurator==<version>
    ```

5. Upload to PyPI:
    ```bash
    twine upload dist/*
    ```
    `twine` will prompt for PyPI credentials, or read them from `~/.pypirc` / the
    `TWINE_USERNAME` and `TWINE_PASSWORD` (or `TWINE_API_KEY`) environment variables. Using a
    scoped [PyPI API token](https://pypi.org/help/#apitoken) as the password (with username
    `__token__`) is recommended over a personal password.

6. Tag the release in git and push the tag, e.g.:
    ```bash
    git tag v<version>
    git push origin v<version>
    ```

There is currently no automated release workflow — publishing is a manual, local step.
