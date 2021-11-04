# This is a helper class
#
#

import string
from random import randrange



# should create an instance of the class so that we keep the state & dictionary

class DictionaryTraverser:
	# The caller is responsible for checking the size of the left/right discionary
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


	def emit(self, prev_eval_result=False):
		'''Emits next character based on the result of the previous execution'''
		# if self.last_char != '':
		# 	if prev_eval_result:
		# 		(c, left, right) = self.__get_random_split(self.left)




		print('Emitting')
		(c, left, right) = self.get_random_split(self.dict)
		print(c)
		print(left)
		print(right)
		# should rerturn c and size of left/right




	
dt = DictionaryTraverser(string.ascii_lowercase)
print(string.ascii_lowercase)
print(dt.get_random_split())


