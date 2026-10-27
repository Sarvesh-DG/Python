import unittest
import sys
import types
from unittest.mock import Mock, call, patch

from fetch_employees import fetch_employees


class TestFetchEmployees(unittest.TestCase):
    def setUp(self):
        self.connection = Mock()
        self.cursor = Mock()
        self.connection.cursor.return_value = self.cursor
        patcher = patch.dict("os.environ", {
            "DB_HOST": "localhost", "DB_USER": "tester",
            "DB_PASSWORD": "secret", "DB_NAME": "employees",
        })
        patcher.start()
        self.addCleanup(patcher.stop)
        self.mysql_stub = types.ModuleType("mysql")
        self.connector_stub = types.ModuleType("mysql.connector")
        self.connector_stub.connect = Mock(return_value=self.connection)
        self.mysql_stub.connector = self.connector_stub
        self.modules_patch = patch.dict(sys.modules, {
            "mysql": self.mysql_stub,
            "mysql.connector": self.connector_stub,
        })
        self.modules_patch.start()
        self.addCleanup(self.modules_patch.stop)
        self.connect = self.connector_stub.connect

    def test_yields_in_batches_and_closes_resources(self):
        first, second = (1, "Lee"), (2, "Mina")
        self.cursor.fetchmany.side_effect = [[first], [second], []]
        self.assertEqual(list(fetch_employees(1)), [first, second])
        self.assertEqual(self.cursor.fetchmany.call_args_list, [call(1)] * 3)
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()
        self.connect.assert_called_once()

    def test_empty_query_result(self):
        self.cursor.fetchmany.return_value = []
        self.assertEqual(list(fetch_employees()), [])
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_invalid_batch_size(self):
        for invalid in (0, -1, 1.5, True):
            with self.subTest(batch_size=invalid):
                with self.assertRaises(ValueError):
                    list(fetch_employees(invalid))
        self.connect.assert_not_called()

    def test_missing_credentials(self):
        with patch.dict("os.environ", {"DB_USER": "", "DB_PASSWORD": ""}):
            with self.assertRaises(RuntimeError):
                list(fetch_employees())
        self.connect.assert_not_called()

    def test_query_failure_closes_resources(self):
        self.cursor.execute.side_effect = RuntimeError("query failed")
        with self.assertRaisesRegex(RuntimeError, "query failed"):
            list(fetch_employees())
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_connect_failure_propagates(self):
        self.connect.side_effect = RuntimeError("unavailable")
        with self.assertRaisesRegex(RuntimeError, "unavailable"):
            list(fetch_employees())


if __name__ == "__main__":
    unittest.main()
