import unittest


class TestExpenseDatabase(unittest.TestCase):
    def test_CRUD(self):
        database_factory = ExpenseDatabaseFactory()
        expense_database = database_factory.get_database()

        # create
        # update
        # query
        # delete


if __name__ == "__main__":
    unittest.main()
