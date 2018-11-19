def print_vector(x, y, z):
	print('<%s, %s, %s>' % (x,y,z))


gen_expr = (x * x for x in range(3))

print_vector(*gen_expr)
dict_vec = {'x': 1, 'y': 0, 'z': 1}

print_vector(**dict_vec) 