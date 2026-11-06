import unittest
from extraction import extract_procedures, parse_parameter, split_sql_parameters


class SQLExtractionTests(unittest.TestCase):
    def test_decimal_parameter_keeps_precision_and_scale(self):
        parsed = parse_parameter("IN salary DECIMAL(10, 2)")
        self.assertEqual(parsed["data_type"], "DECIMAL(10,2)")

    def test_parameter_split_ignores_nested_commas(self):
        params = split_sql_parameters("IN amount DECIMAL(10,2), OUT label VARCHAR(30)")
        self.assertEqual(len(params), 2)

    def test_variable_is_not_reported_as_table(self):
        sql = """
        CREATE PROCEDURE p(OUT newStock INT)
        BEGIN
            SELECT stock_quantity INTO newStock FROM products;
        END
        """
        result = extract_procedures(sql)[0]
        self.assertEqual(result["tables"], ["products"])

    def test_nested_begin_end_block(self):
        sql = """
        CREATE PROCEDURE p(IN x INT)
        BEGIN
            IF x > 0 THEN
                BEGIN
                    UPDATE inventory SET qty = qty - x;
                END;
            END IF;
            SELECT * FROM after_if;
        END
        """
        result = extract_procedures(sql)[0]
        self.assertEqual(result["procedure_name"], "p")
        self.assertEqual(result["tables"], ["after_if", "inventory"])

    def test_multiple_procedures_and_parameter_modes(self):
        sql = """
        CREATE PROCEDURE first_proc(IN a INT, OUT b DECIMAL(10,2))
        BEGIN SELECT * FROM alpha; END;
        CREATE PROCEDURE second_proc(INOUT c VARCHAR(20))
        BEGIN UPDATE beta SET name = c; END;
        """
        results = extract_procedures(sql)
        self.assertEqual([p["procedure_name"] for p in results], ["first_proc", "second_proc"])
        self.assertEqual(results[0]["parameters"][1]["mode"], "OUT")
        self.assertEqual(results[1]["parameters"][0]["mode"], "INOUT")
        self.assertEqual(results[1]["tables"], ["beta"])

    def test_comments_do_not_create_fake_table_references(self):
        sql = """
        CREATE PROCEDURE p()
        BEGIN
            -- FROM fake_table
            SELECT * FROM real_table;
        END
        """
        self.assertEqual(extract_procedures(sql)[0]["tables"], ["real_table"])


if __name__ == "__main__":
    unittest.main()
