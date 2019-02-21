import tensorflow as tf 

with tf.Session():
	x = tf.constant([[5, 3.2], [7, 8]])
	z = tf.matmul(x, x)
	result = z.eval()
	ex_tensor = tf.constant(3)

	tf.shape(ex_tensor)
	tf.rank(ex_tensor)
	print(tf.rank(x))