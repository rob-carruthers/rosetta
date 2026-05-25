from collections.abc import Collection


class PackageSet:
    """A set of packages."""

    # TODO(rob): Create class of package with attached files/services
    packages: Collection[str]

    def __init__(self) -> None:
        """Ensure no duplicates in `packages` by converting to set."""
        self.packages = set(self.packages)


class BasePackageSet(PackageSet):
    """The base package set, to be installed on all hosts."""

    packages = (
        "base",
        "btrfs-progs",
        "helix",
        "linux",
        "linux-firmware",
        "networkmanager",
        "openssh",
    )


class EncryptedRootPackageSet(PackageSet):
    packages = ("cryptsetup",)
