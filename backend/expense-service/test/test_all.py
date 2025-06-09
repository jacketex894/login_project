import unittest
import sys
import os
import logging


def setup_logger() -> logging.Logger:
    """
    Set up and return a logger named 'TestRunner' configured to output debug and above level logs to the console.

    Returns:
        logging.Logger: Configured logger instance named 'TestRunner'.
    """

    logger = logging.getLogger("TestRunner")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def run_all_tests():
    """
    Discover and run all unittest test cases in the current directory.
    """

    logger = setup_logger()

    test_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()

    logger.info("Start search and test %s all test case", test_dir)

    suite = loader.discover(start_dir=test_dir, pattern="*test.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    logger.info("=" * 40)
    logger.info(
        "Test summary: ran %d tests, failures %d, errors %d",
        result.testsRun,
        len(result.failures),
        len(result.errors),
    )

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run_all_tests()
