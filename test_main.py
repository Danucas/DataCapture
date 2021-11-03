"""
Main test
"""
from data_capture import DataCapture


def test_main():
    capture = DataCapture()

    capture.add(3)
    capture.add(9)
    capture.add(3)
    capture.add(4)
    capture.add(6)

    stats = capture.build_stats()

    less_than = stats.less(4)
    greater_than = stats.greater(4)
    between = stats.between(3, 6)

    assert less_than == 2, less_than
    assert between == 4, between
    assert greater_than == 2, greater_than

    less_than = stats.less(20)
    greater_than = stats.greater(1)
    between = stats.between(3, 6)

    assert less_than == 5, less_than
    assert between == 4, between
    assert greater_than == 5, greater_than


def test_exponential_forward():
    capture = DataCapture()

    capture.add(3)
    capture.add(9)
    capture.add(3)
    capture.add(4)
    capture.add(6)

    stats = capture.build_stats()

    less_than = stats.less(4)
    greater_than = stats.greater(4)
    between = stats.between(3, 6)

    assert less_than == 2, less_than
    assert between == 4, between
    assert greater_than == 2, greater_than

    less_than = stats.less(20)
    greater_than = stats.greater(1)
    between = stats.between(-2, 90)

    assert less_than == 5, less_than
    assert between == 5, between
    assert greater_than == 5, greater_than
