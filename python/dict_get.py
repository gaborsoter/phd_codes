ages = {
	'Mary'		: 31, 
	'Jonathan'	: 28,
	'Dick'		: 51
}

# bad way 
# if 'Dick' in ages:
# 	age = ages['Dick']
# else:
# 	age = 'Unkown' 

age = ages.get('Dick', 'Unknown')

print(age)