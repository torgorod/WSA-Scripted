import pytest
import string

from wsa_scripted.dictionary_traverser import DictionaryTraverser


def test_get_random_split():
	dict = string.ascii_lowercase
	dt = DictionaryTraverser(dict)
	(c, left_size, right_size) = dt.get_random_split()
	assert (left_size + 1 + right_size)==len(dict)

def split_till_found(dt, dict, letter):
	(c, left_size, right_size) = dt.get_random_split()
	if c > letter:
		if left_size > 0:
			return split_till_found(dt, dt.left, letter)
		else:
			raise Exception("What? Nonsense")
	elif c < letter:
		if right_size > 0:
			return split_till_found(dt, dt.right, letter)
		else:
			raise Exception("Also not right!")
	elif c == letter:
		return c

def test_word_guessing():
	word = 'TraversingTheDict'
	dict = string.ascii_uppercase + string.ascii_lowercase
	dt = DictionaryTraverser(dict)
	resolved_word = ''
	for i in range(0, len(word)):
		resolved_word += (split_till_found(dt, dict, word[i]))
	assert resolved_word == word
