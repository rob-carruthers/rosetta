from collections.abc import Sequence
from pathlib import Path

from .packageset import (
    BasePackageSet,
    EncryptedRootPackageSet,
    GuiPackageSet,
    LaptopPackageSet,
    NvidiaPackageSet,
    PackageSet,
    PackageWithFiles,
    RobPCPackageSet,
)


class Host:
    def __init__(self, name: str, packagesets: Sequence[PackageSet]) -> None:
        """Create instance attributes for host."""
        self.name = name
        self.packages: set[str | PackageWithFiles] = set().union(*[p.packages for p in packagesets])

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

    def check_files_exist(self):
        for package in self.packages:
            if isinstance(package, str):
                continue
            files = package.get_per_host_files(Path("./hosts"), "rob-pc")
            print(files)


HOSTS = {
    "rob-laptop": Host(
        "rob-laptop",
        [BasePackageSet(), EncryptedRootPackageSet(), LaptopPackageSet(), GuiPackageSet()],
    ),
    "rob-pc": Host(
        "rob-pc",
        [BasePackageSet(), NvidiaPackageSet(), GuiPackageSet(), RobPCPackageSet()],
    ),
}

if __name__ == "__main__":
    print(HOSTS["rob-pc"])
    HOSTS["rob-pc"].write_package_list(Path("./test.txt"))
    HOSTS["rob-pc"].check_files_exist()
