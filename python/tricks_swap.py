# Bad way
# x = 10
# y = -10 
# print('Before: x = %d, y = %d' % (x,y))

# tmp = y
# y = x
# x = tmp
# print('After: x = %d, y = %d' % (x,y))

# good way
x = 10
y = -10 
x, y = y, x

print(x, y)