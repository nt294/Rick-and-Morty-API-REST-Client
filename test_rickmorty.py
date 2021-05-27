import unittest
import unittest.mock
import rickmorty

class test_rickmorty(unittest.TestCase):

    def test_1(self):
    	# Uses mock to emulate user input, i.e. the user pressing 1 and 2 when 
    	# asked if they wish to continue or exit 
    	with unittest.mock.patch('builtins.input', return_value="1"):
    		# The function should return True if the user enters "1"
    		self.assertTrue(rickmorty.user_continue())
    	with unittest.mock.patch('builtins.input', return_value="2"):
    		# The function should return False if the user enters "2"
    		self.assertFalse(rickmorty.user_continue())	
    	
if __name__ == '__main__':
    unittest.main()    