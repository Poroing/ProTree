# -*- coding:utf-8 -*-
from math import floor

class SuccesiveInterval(object):
	"""Container that store values linked to closely wraped interval

	One value is asigned to each interval.
	the end of one interval is begining of the following one.
	Therefore only one number is needed to indicate the end of an interval.
	Each interval is defined by the end of the previous interval and it's own
	end.
	"""

	def __init__(self, iterable=None):
		"""Create a SuccesiveInterval collection

		Create the SuccesiveInterval object from an iterable or nothing.
		The iterable must iterate on, pair, random access collection of length
		2.
		The first value of the pair is the end of the interval at which the
		second value will be linked.

		Args:
			iterable: Iterable of pair which will create the interval and their
				value.
		"""
		if iterable is None:
			self.__container = []
		else:
			self.__container = list(iterable)
			self.__container.sort(key=lambda x: x[0])

	def get(self, key, default=None):
		"""Return the value linked to the interval in which key belong.

		Args:
			key: A number for which the belonging interval's linked value
			default: The value returned if key does not belong to any interval

		Return:
			The value linked to the interval in which key belong.
		"""
		place = self.getInterval(key)
		if place is None:
			return default
		return self.__container[place][1]

	def getInterval(self, key, left=0, right=None):
		"""Return the index of the interval in which key belong

		Args:
			key: A number for which the index of the belonging interval is
				searched.
			left: An integer indicating the lowest index of the indexes it will
				search for
			right: An integer indicating the highest index of the indexes it
				will seach for

		Return:
			The index of the interval in which key belong.
			Or None if no interval where find for the number key.
		"""
		if right is None:
			right = len(self.__container) - 1

		if right < left:
			return None

		mid = floor((left + right) / 2)
		#Check if the key is in the middle interval
		if self.__container[mid][0] >= key:
			if mid == 0 or self.__container[mid - 1][0] < key:
				return mid
			#The key is not in the interval
			return self.getInterval(key, left, mid - 1) #Check at the left
		return self.getInterval(key, mid + 1, right) #Check at the right

	def add(self, pair):
		"""Add an interval and it's linked value to the collection

		Args:
			pair: A random access collection with the first value being the
				end of the interval and the secong the value being the value
				which will be linked to the interval.
		"""
		if len(pair) != 2:
			raise ValueError('the value added must be a pair of a number and'
				'any value')
		place = self.getInterval(pair[0])
		if place is None:
			self.__container.append(pair)
		else:
			self.__container.insert(place, pair)

	def __delitem__(self, key):
		"""Delete the interval in which key belong"""
		del self.__container[self.getInterval(key)]

	def __getitem__(self, key):
		"""Return the value of the interval in which key belong"""
		return self.get(key)

	def __repr__(self):
		return repr(self.__container)

	def __str__(self):
		return str(self.__container)