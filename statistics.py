class Statistics:
    def __init__(self, input_array = None):
        self.input_array = input_array

    def sum_slice(self, array=None, s=0, e=None):
        if array is None:
            array = self.input_array
        if e is None:
            e = len(array) - 1
        return sum(array[s:e])


