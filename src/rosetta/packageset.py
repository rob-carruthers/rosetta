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
        "base-devel",
        "bash-completion",
        "btrfs-progs",
        "chezmoi",
        "dosfstools",
        "efibootmgr",
        "git",
        "helix",
        "htop",
        "lazygit",
        "linux",
        "linux-firmware",
        "ncdu",
        "networkmanager",
        "openssh",
        "starship",
        "sudo",
        "uv",
    )


class EncryptedRootPackageSet(PackageSet):
    """Packages needed for an encrypted rootfs."""

    packages = ("cryptsetup",)


class LaptopPackageSet(PackageSet):
    """Packages required for laptop."""

    packages = ("acpi", "brightnessctl")
