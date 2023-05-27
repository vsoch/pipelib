from pipelib.wrappers.version import VersionWrapper


def test_versionwrapper() -> None:
    """
    Test basic functionality for VersionWrapper
    """
    major = VersionWrapper("3")
    major_minor = VersionWrapper("3.2")
    major_minor_patch = VersionWrapper("3.2.5")
    major_minor_patch_dup = VersionWrapper("3.2.5")

    assert major.version == [3]
    assert major_minor.version == [3, 2]
    assert major_minor_patch.version == [3, 2, 5]

    assert major < major_minor
    assert major_minor < major_minor_patch

    assert hash(major_minor_patch_dup) == hash(major_minor_patch_dup)
