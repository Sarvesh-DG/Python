
import unittest
from unittest.mock import patch, Mock

from fetch_employees import fetch_employees


class TestFetchEmployees(unittest.TestCase):

    def setUp(self):
        self.connection = Mock()
        self.cursor = Mock()

        self.connection.cursor.return_value = self.cursor

        self.connect_patcher = patch(
            "fetch_employees.m.connect",
            return_value=self.connection
        )
        self.mock_connect = self.connect_patcher.start()
        self.addCleanup(self.connect_patcher.stop)

    def test_fetch_employees(self):
        emp1 = (1, "John")
        emp2 = (2, "Alice")

        self.cursor.fetchmany.side_effect = [
            [emp1, emp2],
            []
        ]

        result = list(fetch_employees())

        self.assertEqual(result, [emp1, emp2])
        self.cursor.execute.assert_called_once_with(
            "Select * from employees"
        )
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_batch_size(self):
        self.cursor.fetchmany.side_effect = [
            [(1, "John")],
            []
        ]

        list(fetch_employees(batch_size=1))

        self.assertEqual(
            self.cursor.fetchmany.call_args_list,
            [unittest.mock.call(1), unittest.mock.call(1)]
        )

    def test_empty_database_result(self):
        self.cursor.fetchmany.return_value = []

        result = list(fetch_employees())

        self.assertEqual(result, [])
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_database_cleanup_on_error(self):
        self.cursor.execute.side_effect = RuntimeError(
            "Database query failed"
        )

        with self.assertRaisesRegex(
            RuntimeError, "Database query failed"
        ):
            list(fetch_employees())

        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_connection_failure(self):
        self.mock_connect.side_effect = RuntimeError(
            "Connection failed"
        )

        with self.assertRaisesRegex(
            RuntimeError, "Connection failed"
        ):
            list(fetch_employees())


if __name__ == "__main__":
    unittest.main()
