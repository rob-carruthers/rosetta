from collections.abc import Sequence
from pathlib import Path

from .packageset import (
    BasePackageSet,
    EncryptedRootPackageSet,
    LaptopPackageSet,
    PackageSet,
    PackageWithFiles,
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


HOSTS = {
    "rob-laptop": Host(
        "rob-laptop", [BasePackageSet(), EncryptedRootPackageSet(), LaptopPackageSet()]
    )
}

if __name__ == "__main__":
    print(HOSTS["rob-laptop"])
    HOSTS["rob-laptop"].write_package_list(Path("./test.txt"))
