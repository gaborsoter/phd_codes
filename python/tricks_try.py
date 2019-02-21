print('Converting!')

string = '1'

try:
	print(int(string))
except: 
	print('Conversion failed!')
else: # if no except
	print('Conversion successful')
finally: # always
	print('done')
