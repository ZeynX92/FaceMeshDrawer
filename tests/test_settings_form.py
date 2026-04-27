import pytest
from settings_form import is_valid_rgb


@pytest.mark.parametrize("color_string, expected",
                         [
                             ("255,0,0", True),
                             ("0,255,0", True),
                             ("100,150,200", True),
                             ("256,0,0", False),
                             ("0,0", False),
                             ("abc,def,ghi", False),
                             ("1,2,3,4", False),
                         ])
def test_is_valid_rgb(color_string, expected):
    assert is_valid_rgb(color_string) == expected
