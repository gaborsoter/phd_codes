needle = 'd'
haystack = ['a', 'b', 'c', 'd']


# bad way
# found = False
# for letter in haystack:
# 	if needle == letter:
# 		print('Found!')
# 		found = True
# 		break
# if not found:
# 	print('Not found!')

for letter in haystack:
	if needle == letter:
		print('Found!')
		break
else: # if no break occured
	print('not found!')