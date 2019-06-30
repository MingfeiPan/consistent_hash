import sys
import hashlib
import bisect
import operator

class ChException(Exception):

	pass

class Consistenthash:

	def __init__(self, node_list_with_weight):

		if not isinstance(node_list_with_weight, dict):
			raise TypeError('node_list_with_weight should be a dict')

		self.factor = 40
		self.nodes = node_list_with_weight
		self.ring = {}
		self.total_wight = 0
		self.sorted_keys = []

		self._init_ring()

	def _init_ring(self):

		"""
		generates ring
		"""

		for node, weight in self.nodes.items():
			factor = self.factor * weight
			for i in range(factor):
				for j in range(4):
					_key = self._gen_key('{}-{}'.format(node, i), lambda a: a + j * 4)
					self.ring[_key] = node
					self.sorted_keys.append(_key)

		self.sorted_keys.sort()

	def get_ring(self):
		
		return self.ring

	def get_node(self, key):

		"""
		get a proper node from ring for the key
		"""

		if not isinstance(key, str):
			raise TypeError('key should be a str')

		if not self.ring:
			return None

		_key = self._gen_key(key, lambda a: a)
		pos = bisect.bisect(self.sorted_keys, _key)
		if pos == len(self.nodes):
			#return start pos
			return self.ring[self.sorted_keys[0]]
		return self.ring[self.sorted_keys[pos]]

	def add_node(self, node_list_with_weight):

		"""
		add nodes to the ring
		"""
		if not isinstance(node_list_with_weight, dict):
			raise TypeError('node_list_with_weight should be a dict')		

		self.nodes.update(node_list_with_weight)
		for node, weight in node_list_with_weight.items():
			factor = self.factor * weight
			for i in range(factor):
				for j in range(4):
					_key = self._gen_key('{}-{}'.format(node, i), lambda a: a + j * 4)
					self.ring[_key] = node
					self.sorted_keys.append(_key)

		self.sorted_keys.sort()

	def del_node(self, node_list):

		"""
		remove nodes from ring
		"""

		if not isinstance(node_list, list):
			raise TypeError('node_list should be a list')
		for node in node_list:
			weight = self.nodes.get(node, None)
			if not weight:
				continue
			factor = self.factor * weight
			for i in range(factor):
				for j in range(4):
					_key = self._gen_key('{}-{}'.format(node, i), lambda a: a + j * 4)
					self.ring.pop(_key)
					self.sorted_keys.remove(_key)

		self.sorted_keys.sort()			

	def _gen_key(self, key, func):

		"""
		generates key
		"""

		_str_key = self._key_md5(key)
		# get 4 bytes of md5 hash, return as 32 bits binary  , maximum ->2**32 - 1
		return (_str_key[func(0)] | _str_key[func(1)] << 8 | _str_key[func(2)] << 16 | _str_key[func(3)] << 24)

		


	def _key_md5(self, key):

		"""
		md5 hash func, returned as sequence of int of each unicode chr
		"""

		if not isinstance(key, str):
			raise TypeError('key should be in the form of string')
		m = hashlib.md5()
		m.update(key.encode())
		return [i if isinstance(i ,int) else ord(i) for i in m.digest()]



if __name__ == '__main__':

	test = Consistenthash({'172.17.5.114:11211':1, '172.17.5.115:11211':2, '172.17.5.116:11211':1})
	print(test.get_ring())
	print(test.get_node('test'))
	test.add_node({'172.17.5.117:11211':1, '172.17.5.118:11211':2})
	print(test.get_ring())
	print(test.get_node('test'))
	test.del_node(['172.17.5.118:11211'])
	print(test.get_ring())
	print(test.get_node('test'))
	# print(test._init_ring('test'))%  