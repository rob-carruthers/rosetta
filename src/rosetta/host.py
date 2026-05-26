"""Host definitions and operations."""

from collections.abc import Sequence
from pathlib import Path

from .packageset import (
    BasePackageSet,
    DisplayManagerSet,
    EncryptedRootPackageSet,
    GuiPackageSet,
    LaptopPackageSet,
    MangoDesktopSet,
    NvidiaPackageSet,
    PackageSet,
    PackageWithFiles,
    RobPCPackageSet,
)


class Host:
    """Definition of a host."""

    def __init__(self, name: str, packagesets: Sequence[type[PackageSet]]) -> None:
        """Create instance attributes for host."""
        self.name = name
        self.packages: set[str | PackageWithFiles] = set().union(
            *[p().flatten() for p in packagesets],
        )
        self.packages |= BasePackageSet().flatten()

    def __repr__(self) -> str:
        """Pretty repr for Host.

        Returns
        -------
        str

        """
        sorted_packages = sorted(
            p.package if isinstance(p, PackageWithFiles) else p for p in self.packages
        )
        return f"Host(name={self.name}, packages={sorted_packages})"

    def write_package_list(self, output_path: Path) -> None:
        """Write the Host's package list to a newline-separated text file."""
        packages = [p.package if isinstance(p, PackageWithFiles) else p for p in self.packages]
        packages.sort()
        output_path.parent.mkdir(exist_ok=True, parents=True)

        with output_path.open("w", encoding="utf-8") as f:
            f.writelines("\n".join(packages))
            f.write("\n")

    def check_files_exist(self, config_base_dir: Path, hostname: str) -> None:
        """Check if accompanying files exist for all PackageWithFiles."""
        for package in self.packages:
            if isinstance(package, str):
                continue
            package.get_per_host_files(config_base_dir, hostname)

    def install_files(self, config_base_dir: Path, hostname: str, *, dry_run: bool = False) -> None:
        """Install files for all PackageWithFiles."""
        for package in self.packages:
            if isinstance(package, str):
                continue
            for file in package.get_per_host_files(config_base_dir, hostname):
                file.install(dry_run=dry_run)


HOSTS = {
    "rob-laptop": Host(
        "rob-laptop",
        [
            EncryptedRootPackageSet,
            LaptopPackageSet,
            GuiPackageSet,
            MangoDesktopSet,
            DisplayManagerSet,
        ],
    ),
    "rob-pc": Host(
        "rob-pc",
        [NvidiaPackageSet, GuiPackageSet, RobPCPackageSet, MangoDesktopSet, DisplayManagerSet],
    ),
}

if __name__ == "__main__":
    hostname = "rob-pc"
    hosts_path = Path("./hosts")
    print(HOSTS[hostname])
    HOSTS[hostname].write_package_list(Path("./test.txt"))
    HOSTS[hostname].check_files_exist(hosts_path, hostname)
    HOSTS[hostname].install_files(hosts_path, hostname, dry_run=True)
