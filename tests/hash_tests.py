import sys
sys.path.append('..')
from consistent_hash.consistent_hash import Consistenthash


def test_server():

	ch = Consistenthash({'172.17.5.114:11211':1, '172.17.5.115:11211':2, '172.17.5.116:11211':1})

	excepted = '172.17.5.116:11211'
	node = ch.get_node('test_key')
	assert excepted == node





