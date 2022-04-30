from pager import *

def test_truncate():
    assert truncate(' ', ['AA','AB','AD'], 5) == 'AA AB'
