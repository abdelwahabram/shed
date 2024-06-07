import pytest, os, filecmp

from pathlib import Path

def test_create():
    exit = os.system("shed-create")
    
    expected_dir = Path().joinpath("expected-ouput/.shed")
    output_dir = Path().joinpath(".shed")
    
    comparison_object = filecmp.dircmp(output_dir, expected_dir)
    
    
    assert len(comparison_object.diff_files) == 0

def test_create2():
    exit = os.system("shed-create")
    assert exit == False
    