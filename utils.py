"""
Utils
Creates test samples
"""
from random import random
from data_capture import DataCapture
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import time
import json


time_function = time.time


def create_capture(array_length, base_value=100) -> tuple:
    """
    Creates a capture with an array_length with values between base_value
    :param array_length: the length for the test collections
    :param base_value: the range of values in the collection
    :return: (capture_object, the add case results->used by the plot)
    """
    capture = DataCapture()
    capture.test = True
    value = round(random() * base_value - (base_value / 2))

    tic1 = time_function()
    capture.add(value)
    toc1 = time_function()

    tic2 = time_function()
    capture.add_test(value)
    toc2 = time_function()

    add_avg = toc1 - tic1
    test_add_avg = toc2 - tic2

    for i in range(int((array_length / 2) - 1)):
        value = round(random() * base_value - (base_value / 2))
        tic1 = time_function()
        capture.add(value)
        toc1 = time_function()

        tic2 = time_function()
        capture.add_test(value)
        toc2 = time_function()

        add_avg = (add_avg + (toc1 - tic1)) / 2
        test_add_avg = (add_avg + (toc2 - tic2)) / 2

    # repeat all values once at least
    for value in capture.test_collection.copy():
        tic1 = time_function()
        capture.add(value)
        toc1 = time_function()

        tic2 = time_function()
        capture.add_test(value)
        toc2 = time_function()

        add_avg = (add_avg + (toc1 - tic1)) / 2
        test_add_avg = (add_avg + (toc2 - tic2)) / 2

    add_case = ('add()', add_avg, test_add_avg)
    print('\t', add_case[0], add_case[1], 'test_add', add_case[2])

    return capture, add_case


def capture_and_query(size, status_percent) -> list:
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
    case = [status_percent]
    capture, add_case = create_capture(size, 1000000)
    case.append(add_case)

    tic = time_function()
    stats = capture.build_stats()
    toc = time_function()

    case.append(('build_stats()', (toc - tic)))
    print('\t', case[2][0], case[2][1])

    tic1 = time_function()
    exp_lt = sum(y < 4 for y in capture.test_collection)
    toc1 = time_function()

    tic2 = time_function()
    lt = stats.less(4)
    toc2 = time_function()

    msg = f'LT -> 4, exp: {exp_lt}, actual: {lt}.\n{json.dumps(capture.test_collection, indent=2)}'
    assert lt == exp_lt, msg

    case.append(('less()', (toc2 - tic2), (toc1 - tic1)))
    print('\t', case[3][0], case[3][1], 'iterative', case[3][2])

    tic1 = time_function()
    exp_gt = sum(y > 4 for y in capture.test_collection)
    toc1 = time_function()

    tic2 = time_function()
    gt = stats.greater(4)
    toc2 = time_function()

    msg = f'GT -> 4, exp: {exp_gt}, actual: {gt}.\n{json.dumps(capture.test_collection, indent=2)}'
    assert gt == exp_gt, msg

    case.append(('greater()', (toc2 - tic2), (toc1 - tic1)))

    tic1 = time_function()
    exp_bt = sum(100 <= n <= 1000 for n in capture.test_collection)
    toc1 = time_function()

    tic2 = time_function()
    between = stats.between(100, 1000)
    toc2 = time_function()

    msg = f'BT -> 100 - 1000, exp: {exp_bt}, actual: {between}, {capture.test_collection}'
    assert between == exp_bt, msg

    case.append(('between()', (toc2 - tic2), (toc1 - tic1)))

    case.append(('min_and_max', (capture.min, capture.max)))
    print('\t', case[4][0], case[4][1], 'iterative', case[4][2])

    return case


def run_and_plot(title, initial_value=2, max_exp=20, reverse=False, exponential=False):
    """
    Uses the arguments to create a direction test over n*exp or n**exp values
    :param title: used by the window
    :param initial_value: min initial value for the test
    :param max_exp: maxim to try
    :param reverse: do we want it backwards?
    :param exponential: do we wanted exponential?
    :return: None
    """
    cases_results = []

    direction = (
        range(max_exp, 1, -1)
        if reverse
        else (
            range(
                1,
                max_exp+1,
                (
                    1
                    if exponential
                    else int(max_exp / 20)
                )
            )
        )
    )

    for exp in direction:
        if exponential:
            size = pow(initial_value, exp)
        else:
            size = initial_value * exp

        if reverse:
            percent = (max_exp - exp) * 100 / max_exp
        else:
            percent = exp * 100 / max_exp

        case = capture_and_query(size, percent)
        cases_results.append(case)
        print(f'\n{round(percent)}% -> ', end='')
        print(f'(values_range: {case[6][1][0]} - {case[6][1][1]}, records: {size})')

    print()

    plot(title, cases_results)


def plot(title, cases_results, filename=None):
    """
    draw a Figure contained in the cases_result object
    :param title: Window's title
    :param cases_results: info about add, greater, less and between metrics
    :return: None
    """
    case_size = [case[0] for case in cases_results]
    add_stats = [case[1][1] for case in cases_results]
    it_add = [case[1][2] for case in cases_results]
    build_stats = [case[2][1] for case in cases_results]
    less_stats = [case[3][1] for case in cases_results]
    it_less = [case[3][2] for case in cases_results]
    greater_stats = [case[4][1] for case in cases_results]
    it_gt = [case[4][2] for case in cases_results]
    between_stats = [case[5][1] for case in cases_results]
    it_bt = [case[5][2] for case in cases_results]

    fig = plt.figure(constrained_layout=True)
    fig.canvas.set_window_title(title)
    fig.tight_layout(pad=4)

    gs = GridSpec(9, 11)

    ax1 = fig.add_subplot(gs[:, :3])
    ax1.set_title('build_stats')
    ax1.set_ylabel('time in secs')
    ax1.plot(case_size, build_stats, color='purple', marker='v')

    ax2 = fig.add_subplot(gs[:4, 4:7])
    ax2.set_title('add')
    ax2.plot(case_size, it_add, color='tab:grey', marker='.')
    ax2.plot(case_size, add_stats, color='tab:green', marker='o')

    ax3 = fig.add_subplot(gs[5:, 4:7])
    ax3.set_title('less')
    ax3.plot(case_size, it_less, color='tab:grey', marker='.')
    ax3.plot(case_size, less_stats, color='tab:red', marker='o')

    ax4 = fig.add_subplot(gs[:4, 8:])
    ax4.set_title('greater')
    ax4.plot(case_size, it_gt, color='tab:grey', marker='.')
    ax4.plot(case_size, greater_stats, color='tab:orange', marker='o')

    ax5 = fig.add_subplot(gs[5:, 8:])
    ax5.set_title('between')
    ax5.plot(case_size, it_bt, color='tab:grey', marker='.')
    ax5.plot(case_size, between_stats, color='tab:cyan', marker='o')
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
