import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Collection


@dataclass(frozen=True)
class FileToInstall:
    install_location: str
    mode: int
    source: Path | None = None

    def install(self, *, dry_run: bool) -> None:
        if self.source is None:
            raise ValueError

        if dry_run:
            print(f"would copy {self.source} to {self.install_location} with mode {oct(self.mode)}")
            return

        shutil.copy2(self.source, self.install_location)
        Path(self.install_location).chmod(self.mode)


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
    packages: "Collection[str | PackageWithFiles | PackageSet]"

    def __init__(self) -> None:
        """Ensure no duplicates in `packages` by converting to set."""
        self.packages = set(self.packages)

    def flatten(self) -> set[str | PackageWithFiles]:
        packages: list[str | PackageWithFiles] = []

        for package in self.packages:
            if isinstance(package, PackageSet):
                packages.extend(package.flatten())
            else:
                packages.append(package)

        return set(packages)


class BasePackageSet(PackageSet):
    """The base package set, to be installed on all hosts."""

    packages = (
        PackageWithFiles(
            "base",
            (
                FileToInstall(install_location="/etc/fstab", mode=0o644),
                FileToInstall(install_location="/etc/udev/rules.d/99fast_charge.rules", mode=0o644),
            ),
        ),
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
        "less",
        "linux",
        "linux-firmware",
        "ncdu",
        "networkmanager",
        "openssh",
        "ripgrep",
        "starship",
        "sudo",
        "tmux",
        "uv",
    )


class EncryptedRootPackageSet(PackageSet):
    """Packages needed for an encrypted rootfs."""

    packages = ("cryptsetup",)


class FontsSet(PackageSet):
    """Fonts."""

    packages = ("noto-fonts", "noto-fonts-emoji", "otf-font-awesome", "ttf-jetbrains-mono-nerd")


class GuiPackageSet(PackageSet):
    """Packages needed for any GUI system."""

    packages = ("avahi", "nss-mdns", "pulsemixer", "syncthing")


class LaptopPackageSet(PackageSet):
    """Packages required for laptop."""

    packages = ("acpi", "brightnessctl")


class NvidiaPackageSet(PackageSet):
    """NVIDIA drivers."""

    packages = ("nvidia-open",)


class RobPCPackageSet(PackageSet):
    """Packages specific to rob-pc."""

    packages = (
        NvidiaPackageSet(),
        "ario",
        PackageWithFiles(
            "ch57x-keyboard-tool",
            (FileToInstall("/etc/udev/rules.d/99utility_keys.rules", mode=0o644),),
        ),
        PackageWithFiles(
            "ddcutil",
            (
                FileToInstall("/usr/local/bin/monitor-switch.sh", mode=0o755),
                FileToInstall("/etc/udev/rules.d/99monitor_switch.rules", mode=0o644),
            ),
        ),
        "mpd",
        "mpc",
    )


class WaylandAppsSet(PackageSet):
    packages = (
        FontsSet(),
        "blueman",
        "dogecoin-qt",
        "firefox",
        "foot",
        "gtklock",
        "musescore",
        "pavucontrol",
        "qutebrowser",
        PackageWithFiles(
            "swayidle",
            (FileToInstall("/usr/local/bin/idle-command.sh", mode=0o755),),
        ),
        "syncthingtray",
        "waybar",
        "wl-clipboard",
        "wlopm",
        "wofi",
    )


class DisplayManagerSet(PackageSet):
    packages = (
        "cage",
        PackageWithFiles(
            "greetd",
            (FileToInstall("/etc/greetd/config.toml", 0o644),),
        ),
        "greetd-regreet",
        "seatd",
    )


class MangoDesktopSet(PackageSet):
    packages = (WaylandAppsSet(), "mangowm", "memphis98-icon-theme-git", "pcmanfm-qt")
