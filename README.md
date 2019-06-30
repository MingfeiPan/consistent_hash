### hashing

a consistent hashing implement using [libketama](https://github.com/RJ/ketama) in python 

### install   

python setup.py install  

### usage  

```

from consistent_hash import consistent_hash

#init 

ch = Consistenthash({'172.17.5.114:11211':1, '172.17.5.115:11211':2, '172.17.5.116:11211':1})

#get a node
node = ch.get_node('test_key')

#add more nodes
add_node({'172.17.5.117:11211':1, '172.17.5.118:11211':2})

#del nodes
del_node(['172.17.5.118:11211'])

```



