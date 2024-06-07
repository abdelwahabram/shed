import pytest, subprocess
from pathlib import Path
from filecmp import dircmp


def test_add():
    path1 = Path().joinpath("test.txt")
    path2 = Path().joinpath("test2.txt")
    
    # os.system("shed-add")
    subprocess.run(["shed-create"])
    subprocess.run(["shed-add", path1, path2])
    
    output_dir = Path().joinpath(".shed/blocks")
    expected_dir = Path().joinpath("expected-output/.shed/blocks")
    
    comparison_object = dircmp(output_dir, expected_dir)
    
    assert len(comparison_object.left_only) == 0 and len(comparison_object.right_only) == 0
    