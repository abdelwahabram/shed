import pytest, subprocess
from freezegun import freeze_time
from filecmp import dircmp
from pathlib import Path

# @freeze_time("2024-06-06 00:15:18")
def test_build():
    # the decorator can't change time for the system time it can only mimic datetime module for tests
    with freeze_time("2024-06-06 00:15:18"):
        subprocess.run(["shed-build", "commit test files"])
    
    output = Path().joinpath(".shed/blocks")
    expected = Path().joinpath("expected-ouput/.shed/blocks")

    comparison_object  = dircmp(output, expected)
    assert comparison_object.right_only == ["67facc3ee97d8b586479ca71223f5bc5ef70b078"]
        