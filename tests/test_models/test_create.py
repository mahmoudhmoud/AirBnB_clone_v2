import MySQLdb
import unittest
from console import HBNBCommand

class TestCreateState(unittest.TestCase):
    def setUp(self):
        self.db = MySQLdb.connect(host="localhost", user="hbnb_test", passwd="hbnb_test_pwd", db="hbnb_test_db")
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT COUNT(*) FROM states")
        self.initial_state_count = self.cursor.fetchone()[0]

    def test_create_state(self):
        # Execute the console command here
        console_app = HBNBCommand()
        console_app.do_create("State name=\"California\"")

        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_state_count = self.cursor.fetchone()[0]
        self.assertEqual(final_state_count, self.initial_state_count + 1)

    def tearDown(self):
        self.db.close()
