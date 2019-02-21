# Bad way
# cities = ['Marseille', 'Amsterdam', 'New York', 'London']

# i = 0

# for city in cities:
# 	print(i, city)
# 	i += 1

cities = ['Marseille', 'Amsterdam', 'New York', 'London']

for i, city in enumerate(cities):
	print(i, city)