#!/usr/bin/env python3
"""
DataCapture:

"""


class DataCapture:
    def __init__(self):
        self.unmapped_collection = []
        self.test_collection = []
        self.collection = {}
        self.mapped_collection = {}
        self.min = None
        self.max = None
        self.test = False

    def add(self, number):
        # Used as support to between function
        self.unmapped_collection.append(number)
        self.collection[number] = self.collection[number] + 1 if number in self.collection else 1

        if self.min is None:
            self.min = number
        elif number < self.min:
            self.min = number

        if self.max is None:
            self.max = number
        elif number > self.max:
            self.max = number

    def add_test(self, number):
        # if self.test:
        self.test_collection.append(number)

    def build_stats(self):
        self.min = self.min - 1
        self.max = self.max + 1
        counter = 0
        collection_keys = self.collection.keys()
        for index in range(self.min - 1, self.max + 1):
            self.mapped_collection[index] = counter
            counter += self.collection[index] if index in collection_keys else 0
        return Stats(self)


class Stats:
    def __init__(self, data_capture):
        self.data_capture = data_capture

    def less(self, number):
        if self.data_capture.min <= number <= self.data_capture.max:
            return self.data_capture.mapped_collection[number]
        elif number > self.data_capture.max:
            return self.data_capture.mapped_collection[self.data_capture.max]
        else:
            return 0

    def greater(self, number):
        if self.data_capture.min <= number <= self.data_capture.max:
            return (
                    self.data_capture.mapped_collection[self.data_capture.max]
                    - self.data_capture.mapped_collection[number + 1]
            )
        elif number < self.data_capture.min:
            return self.data_capture.mapped_collection[self.data_capture.max]
        else:
            return 0

    def between(self, start, end):
        return sum(end >= n >= start for n in self.data_capture.unmapped_collection)
