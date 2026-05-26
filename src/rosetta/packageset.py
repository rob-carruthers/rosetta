from pathlib import Path
from collections.abc import Collection, Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FileToInstall:
    install_location: str
    mode: str
    source: Path | None = None


@dataclass(frozen=True)
class PackageWithFiles:
    package: str
    files: tuple[FileToInstall, ...]

    def get_per_host_files(self, config_base_dir: Path, hostname: str) -> tuple[FileToInstall, ...]:
        output = tuple(
            FileToInstall(
                source=config_base_dir / hostname / file.install_location.lstrip("/"),
                install_location=file.install_location,
                mode=file.mode,
            )
            for file in self.files
        )
        for file in output:
            if file.source is None:
                raise TypeError
            if not file.source.exists():
                msg = f"{file.source} does not exist"
                raise FileNotFoundError(msg)

        return output


class PackageSet:
    """A set of packages."""

    # TODO(rob): Create class of package with attached files/services
    packages: Collection[str | PackageWithFiles]

    def __init__(self) -> None:
        """Ensure no duplicates in `packages` by converting to set."""
        self.packages = set(self.packages)


class BasePackageSet(PackageSet):
    """The base package set, to be installed on all hosts."""

    packages = (
        PackageWithFiles("base", (FileToInstall("/etc/fstab", "hi"),)),
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
        "tmux",
        "uv",
    )


class EncryptedRootPackageSet(PackageSet):
    """Packages needed for an encrypted rootfs."""

    packages = ("cryptsetup",)


class GuiPackageSet(PackageSet):
    """Packages needed for any GUI system."""

    packages = ("pulsemixer", "syncthing")


class LaptopPackageSet(PackageSet):
    """Packages required for laptop."""

    packages = ("acpi", "brightnessctl")


class RobPCPackageSet(PackageSet):
    """Packages specific to rob-pc."""

    packages = ("ario", "mpd", "mpc")


class NvidiaPackageSet(PackageSet):
    """NVIDIA drivers."""

    packages = ("nvidia",)
