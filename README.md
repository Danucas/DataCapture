# DataCapture usage instructions
Stats Operator to query comparisons within a list of values

### Requirements
- Python >= 3.8

install dependencies
```bash
(youruser)$ pip3 install requirements.txt
```

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

Also check `run_and_plot` to test over big samples

```python
from utils import run_and_plot
run_and_plot('test_sample', initial_value=2, max_exp=20, exponential=False)
```

```
0% -> (values_range: -23099 - 1234444, records: 6)
         add() 5.885958671569824e-07 test_add 2.942979335784912e-07
         build_stats() 0.02675914764404297
         less() 5.0067901611328125e-06 iterative 1.9073486328125e-05
         greater() 1.9073486328125e-06 iterative 1.9073486328125e-06

10% -> (values_range: -37393 - 82400, records: 6)
         add() 9.173242252538683e-07 test_add 4.586621126269341e-07
         build_stats() 0.18477368354797363
         less() 3.0994415283203125e-06 iterative 6.9141387939453125e-06
         greater() 1.9073486328125e-06 iterative 4.0531158447265625e-06

20% -> (values_range: -489978 - 497864, records: 36)
         add() 4.866417354090161e-07 test_add 2.4332086770450807e-07
         build_stats() 0.16634917259216309
         less() 3.0994415283203125e-06 iterative 3.504753112792969e-05
         greater() 9.5367431640625e-07 iterative 1.4066696166992188e-05

```
