# DataCapture usage instructions
Stats Operator to query comparisons within a list of values

Usage Example
```python
from data_capture import DataCapture

capture = DataCapture()

# add new values to the collection
capture.add(3)
capture.add(45)
capture.add(20)

# Build the Stats instance
stats = capture.build_stats()

# Check for values greater than
print(stats.greater(10))

# Check values less than
print(stats.less(30))

# Check check for values between a range
print(stats.between(4, 28))
```

The output should be something like

```bash
2
2
1
```

Use [utils.py](/utils.py) `create_capture(array_length, values_range)` to create a List[n] values

```python
from utils import create_capture


# Notes that create_capture returns the capture containing the collection
# and the add_case containing the avg processing time for capture.add function
capture, add_case = create_capture(100, 1234)

# capture_and query(size, status_percent):
# return metrics by running a process with a 'size' values collection
# and link it to a 'status_percent' progress scale
"""
    case = [
        0: status_percent,
        1: add_case,
        2: built_stats,
        3: less_than,
        4: greater_than,
    ]
    :param size:
    :param status_percent:
    :return:
"""
from utils import capture_and_query


case_results = capture_and_query(100, 10)
print(case_results)
```

Output should be something like

```bash
    add() 1.992952093840107e-06 test_add 9.964760469200536e-07
    build_stats() 0.18728017807006836
    less() 3.814697265625e-06 iterative 1.8835067749023438e-05
    greater() 3.0994415283203125e-06 iterative 7.867813110351562e-06
```

`plot` will render a matplotlib window to visualize the metrics

```python
from utils import capture_and_query, plot


case_results = [
    capture_and_query(10 ** 2, 25),
    capture_and_query(10 ** 3, 50),
    capture_and_query(10 ** 4, 75),
    capture_and_query(10 ** 5, 100),
]

plot('10 ** range(2 - 5)', case_results)
```

Should draw something like

![](/screenshots/plot_example_1.png)
