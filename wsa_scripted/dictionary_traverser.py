import string
from random import randrange


# DictionaryTraverser comes handy in cases where there is a need to guess an element
# of a dictionary, while there are only indications avaialble on whether a given attempted
# element is located before or after in the dictionary relatively to the correct one
#
# Note: The caller is responsible for checking the size of the left/right discionary!

class DictionaryTraverser:
	def __init__(self, dict):
		self.dict = dict
		self.left = ''
		self.right = ''

	def get_random_split(self, s=None):
		if s == None:
			s=self.dict
		if (len(s) < 1):
			raise Exception("There are no more characters to try.")
		pos = randrange(len(s))
		c = s[pos]
		if pos > 0:
			left = s[:pos]
			if pos < len(s) - 1:
				right = s[pos+1:]
			else:
				right = ''
		else:
			left = ''
			right = s[1:]
		
		self.left = left
		self.right = right

		return (c, len(left), len(right))
