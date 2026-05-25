from collections.abc import Sequence

from .packageset import BasePackageSet, EncryptedRootPackageSet, PackageSet


class Host:
    def __init__(self, name: str, packagesets: Sequence[PackageSet]) -> None:
        """Create instance attributes for host."""
        self.name = name
        self.packages = set().union(*[p.packages for p in packagesets])

    def __repr__(self) -> str:
        """Pretty repr for Host.

        Returns
        -------
        str

        """
        return f"Host(name={self.name}, packages={sorted(self.packages)})"


HOSTS = {"rob-laptop": Host("rob-laptop", [BasePackageSet(), EncryptedRootPackageSet()])}

if __name__ == "__main__":
    print(HOSTS["rob-laptop"])
