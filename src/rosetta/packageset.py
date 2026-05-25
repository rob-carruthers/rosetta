from collections.abc import Collection, Sequence


class PackageSet:
    """A set of packages."""

    # TODO(rob): Create class of package with attached files/services
    packages: Collection[str]

    def __init__(self) -> None:
        """Ensure no duplicates in `packages` by converting to set."""
        self.packages = set(self.packages)


class BasePackageSet(PackageSet):
    """The base package set, to be installed on all hosts."""

    packages = ("base", "linux", "linux-firmware")


class TestPackageSet(PackageSet):
    packages = ("linux", "lazygit")


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


if __name__ == "__main__":
    hostname = "rob-laptop"
    host = Host(hostname, [BasePackageSet(), TestPackageSet()])
    print(host)
