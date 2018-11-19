def foo(required, *args, **kwargs):
	print(required)
	if args:
		print(args)
	if kwargs:
		print(kwargs)


def foo2(x, *arg, **kwargs):
	kwargs['name'] = 'Alice'
	new_args = args + ('extra', )
	bar(x, *new_args, **kwargs)

class Car:
	def __init__(self, color, milage):
		self.color = color
		self.milage = milage

class AlwaysBlueCar:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.color = 'blue'