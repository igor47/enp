import importlib.metadata as importlib_metadata


# NOTE: must match the name in `pyproject.toml`
PACKAGE_NAME: str = "enp"


def get_package_version() -> str:
    """Returns the package version."""
    metadata = importlib_metadata.metadata(PACKAGE_NAME)  # type: ignore
    version = metadata["Version"]

    return version
