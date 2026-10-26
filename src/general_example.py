import time
from typing import Dict, List

    
class GeneralExample():
    def flatten_dictionary(content: Dict) -> List:
        '''
        Example of this function call:
            flatten_dictionary({'key1': [3, 2, 1], 'key2': [42, 55, 10], 'key3': [0, 22]})
            output: [0, 1, 2, 3, 10, 22, 42, 55]
        '''

        return sorted({x for v in content.values() for x in v})


    def load_employee_rec_from_database(self) -> List:
        time.sleep(10)
        sample_emp_record = ['emp001', 'Sam', '100000']
        return sample_emp_record


    def fetch_emp_details(self):
        db_record = self.load_employee_rec_from_database(self)

        emp_details = {
            'empId': db_record[0],
            'empName': db_record[1],
            'empSalary': db_record[2]
        }

        return emp_details


