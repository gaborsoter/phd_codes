import tensorflow as tf 

# placeholder: it is a promise
with tf.Session():
	x = tf.placeholder(tf.float32)
	y = tf.placeholder(tf.float32)
	z = x + y 

	sess = tf.Session()


print(sess.run(z, feed_dict = {x: 3, y: 4.5}))