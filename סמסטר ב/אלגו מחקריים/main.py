from functools import lru_cache
import itertools
import io
import sys

# Decorator for additional functionality
def Decorator(func):
    """
    A decorator to print function execution details.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.
    """
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__} with arguments {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

# Memoization decorator
def memoization(func):
    """
    A memoization decorator to cache function results.

    Args:
        func (callable): The function to be memoized.

    Returns:
        callable: The memoized function.
    """
    cache = {}
    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return memoized_func

class InputHandler:
    def get_data(self):
        """
        Method to get input data.
        """
        raise NotImplementedError

class SingleIntegerInputHandler(InputHandler):
    def __init__(self, number):
        """
        Initialize with a single integer.

        Args:
            number (int): The input number.
        """
        self.number = number

    def get_data(self):
        """
        Get the input number.

        Returns:
            int: The input number.
        """
        return self.number

class ListIntegerInputHandler(InputHandler):
    def __init__(self, numbers):
        """
        Initialize with a list of integers.

        Args:
            numbers (list of int): The input numbers.
        """
        self.numbers = numbers

    def get_data(self):
        """
        Get the input numbers.

        Returns:
            list of int: The input numbers.
        """
        return self.numbers

class OutputHandler:
    def output(self, result):
        """
        Method to handle output.
        """
        raise NotImplementedError

class SingleValueOutputHandler(OutputHandler):
    def output(self, result):
        """
        Output a single value.

        Args:
            result (int): The result value.

        Returns:
            int: The result value.
        """
        return result

class SequenceOutputHandler(OutputHandler):
    def output(self, result):
        """
        Output the entire sequence.

        Args:
            result (list of int): The result sequence.

        Returns:
            list of int: The result sequence.
        """
        return result

class FibonacciAlgorithm:
    def compute(self, number):
        """
        Method to compute Fibonacci.
        """
        raise NotImplementedError

class IterativeFibonacci(FibonacciAlgorithm):
    def compute(self, number):
        """
        Compute Fibonacci iteratively.

        Args:
            number (int): The input number.

        Returns:
            list of int or int: The Fibonacci sequence or the Fibonacci number.
        """
        if number == 0:
            return [0]
        elif number == 1:
            return [0, 1]
        else:
            fib_seq = [0, 1]
            for i in range(2, number + 1):
                fib_seq.append(fib_seq[-1] + fib_seq[-2])
            return fib_seq

class RecursiveFibonacci(FibonacciAlgorithm):
    @memoization
    def compute(self, number):
        """
        Compute Fibonacci recursively with memoization.

        Args:
            number (int): The input number.

        Returns:
            int: The Fibonacci number.
        """
        if number < 2:
            return number
        return self.compute(number - 1) + self.compute(number - 2)

class FibonacciFlyweight:
    def __init__(self):
        """
        Initialize the Flyweight factory.
        """
        self.shared_data = {}

    def get_fibonacci(self, algorithm_type):
        """
        Get the Fibonacci algorithm instance.

        Args:
            algorithm_type (str): The type of algorithm.

        Returns:
            FibonacciAlgorithm: The Fibonacci algorithm instance.
        """
        if algorithm_type not in self.shared_data:
            if algorithm_type == 'iterative':
                self.shared_data[algorithm_type] = IterativeFibonacci()
            elif algorithm_type == 'recursive':
                self.shared_data[algorithm_type] = RecursiveFibonacci()
        return self.shared_data[algorithm_type]

class CapturePrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self._stringio

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout

def main():
    """
    Main function to demonstrate the Fibonacci solution.

    >>> single_input = 5
    >>> list_input = [3, 5, 7]

    >>> input_handlers = [
    ...     SingleIntegerInputHandler(single_input),
    ...     ListIntegerInputHandler(list_input)
    ... ]

    >>> output_handlers = [
    ...     SingleValueOutputHandler(),
    ...     SequenceOutputHandler()
    ... ]

    >>> flyweight_factory = FibonacciFlyweight()

    >>> with CapturePrints() as output:
    ...     for input_handler in input_handlers:
    ...         data = input_handler.get_data()
    ...         for algorithm_type in ['iterative', 'recursive']:
    ...             fib_algo = flyweight_factory.get_fibonacci(algorithm_type)
    ...             if isinstance(data, list):
    ...                 for number in data:
    ...                     if algorithm_type == 'iterative':
    ...                         result = fib_algo.compute(number)
    ...                         result_value = result[-1]
    ...                     else:
    ...                         result = [fib_algo.compute(i) for i in range(number + 1)]
    ...                         result_value = result[-1]
    ...                     for output_handler in output_handlers:
    ...                         if isinstance(output_handler, SingleValueOutputHandler):
    ...                             print(f"Algorithm: {algorithm_type}, Input: {type(input_handler).__name__}, Output: {type(output_handler).__name__} -> {output_handler.output(result_value)}")
    ...                         else:
    ...                             print(f"Algorithm: {algorithm_type}, Input: {type(input_handler).__name__}, Output: {type(output_handler).__name__} -> {output_handler.output(result)}")
    ...             else:
    ...                 number = data
    ...                 if algorithm_type == 'iterative':
    ...                     result = fib_algo.compute(number)
    ...                     result_value = result[-1]
    ...                 else:
    ...                     result = [fib_algo.compute(i) for i in range(number + 1)]
    ...                     result_value = result[-1]
    ...                 for output_handler in output_handlers:
    ...                     if isinstance(output_handler, SingleValueOutputHandler):
    ...                         print(f"Algorithm: {algorithm_type}, Input: {type(input_handler).__name__}, Output: {type(output_handler).__name__} -> {output_handler.output(result_value)}")
    ...                     else:
    ...                         print(f"Algorithm: {algorithm_type}, Input: {type(input_handler).__name__}, Output: {type(output_handler).__name__} -> {output_handler.output(result)}")
    >>> print(output.getvalue().strip())
    Algorithm: iterative, Input: SingleIntegerInputHandler, Output: SingleValueOutputHandler -> 5
    Algorithm: iterative, Input: SingleIntegerInputHandler, Output: SequenceOutputHandler -> [0, 1, 1, 2, 3, 5]
    Algorithm: recursive, Input: SingleIntegerInputHandler, Output: SingleValueOutputHandler -> 5
    Algorithm: recursive, Input: SingleIntegerInputHandler, Output: SequenceOutputHandler -> [0, 1, 1, 2, 3, 5]
    Algorithm: iterative, Input: ListIntegerInputHandler, Output: SingleValueOutputHandler -> 2
    Algorithm: iterative, Input: ListIntegerInputHandler, Output: SequenceOutputHandler -> [0, 1, 1, 2]
    Algorithm: iterative, Input: ListIntegerInputHandler, Output: SingleValueOutputHandler -> 5
    Algorithm: iterative, Input: ListIntegerInputHandler, Output: SequenceOutputHandler -> [0, 1, 1, 2, 3, 5]
    Algorithm: iterative, Input: ListIntegerInputHandler, Output: SingleValueOutputHandler -> 13
    Algorithm: iterative, Input: ListIntegerInputHandler, Output: SequenceOutputHandler -> [0, 1, 1, 2, 3, 5, 8, 13]
    Algorithm: recursive, Input: ListIntegerInputHandler, Output: SingleValueOutputHandler -> 2
    Algorithm: recursive, Input: ListIntegerInputHandler, Output: SequenceOutputHandler -> [0, 1, 1, 2]
    Algorithm: recursive, Input: ListIntegerInputHandler, Output: SingleValueOutputHandler -> 5
    Algorithm: recursive, Input: ListIntegerInputHandler, Output: SequenceOutputHandler -> [0, 1, 1, 2, 3, 5]
    Algorithm: recursive, Input: ListIntegerInputHandler, Output: SingleValueOutputHandler -> 13
    Algorithm: recursive, Input: ListIntegerInputHandler, Output: SequenceOutputHandler -> [0, 1, 1, 2, 3, 5, 8, 13]
    """

    single_input = 5
    list_input = [3, 5, 7]

    input_handlers = [
        SingleIntegerInputHandler(single_input),
        ListIntegerInputHandler(list_input)
    ]

    output_handlers = [
        SingleValueOutputHandler(),
        SequenceOutputHandler()
    ]

    flyweight_factory = FibonacciFlyweight()

    for input_handler in input_handlers:
        data = input_handler.get_data()
        for algorithm_type in ['iterative', 'recursive']:
            fib_algo = flyweight_factory.get_fibonacci(algorithm_type)
            if isinstance(data, list):
                for number in data:
                    if algorithm_type == 'iterative':
                        result = fib_algo.compute(number)
                        result_value = result[-1]
                    else:
                        result = [fib_algo.compute(i) for i in range(number + 1)]
                        result_value = result[-1]
                    for output_handler in output_handlers:
                        if isinstance(output_handler, SingleValueOutputHandler):
                            print(f"Algorithm: {algorithm_type}, Input: {type(input_handler).__name__}, Output: {type(output_handler).__name__} -> {output_handler.output(result_value)}")
                        else:
                            print(f"Algorithm: {algorithm_type}, Input: {type(input_handler).__name__}, Output: {type(output_handler).__name__} -> {output_handler.output(result)}")
            else:
                number = data
                if algorithm_type == 'iterative':
                    result = fib_algo.compute(number)
                    result_value = result[-1]
                else:
                    result = [fib_algo.compute(i) for i in range(number + 1)]
                    result_value = result[-1]
                for output_handler in output_handlers:
                    if isinstance(output_handler, SingleValueOutputHandler):
                        print(f"Algorithm: {algorithm_type}, Input: {type(input_handler).__name__}, Output: {type(output_handler).__name__} -> {output_handler.output(result_value)}")
                    else:
                        print(f"Algorithm: {algorithm_type}, Input: {type(input_handler).__name__}, Output: {type(output_handler).__name__} -> {output_handler.output(result)}")

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
    main()
