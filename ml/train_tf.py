from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)

def cnn_model_fn(features, labels, mode):
    x = tf.reshape(features["x"], [-1, 28, 28, 1])
    x = tf.layers.conv2d(inputs=x, filters=32, kernel_size=[5, 5], padding="same", activation=tf.nn.relu)
    x = tf.layers.max_pooling2d(inputs=x, pool_size=[2, 2], strides=2)
    x = tf.layers.conv2d(inputs=x, filters=64, kernel_size=[5, 5], padding="same", activation=tf.nn.relu)
    x = tf.layers.max_pooling2d(inputs=x, pool_size=[2, 2], strides=2)
    x = tf.reshape(x, [-1, 7 * 7 * 64])
    x = tf.layers.dense(inputs=x, units=1024, activation=tf.nn.relu)
    x = tf.layers.dropout(inputs=x, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)
    x = tf.layers.dense(inputs=x, units=10)
    predictions = {"classes": tf.argmax(input=x, axis=1), "probabilities": tf.nn.softmax(x, name="softmax_tensor")}
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=x)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(loss=loss, global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)
    eval_metric_ops = {"accuracy": tf.metrics.accuracy(labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def main(unused_argv):
    # load
    mnist = tf.contrib.learn.datasets.load_dataset("mnist")
    train_data = mnist.train.images
    train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    eval_data = mnist.test.images
    eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)
    # train
    mnist_classifier = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir="/tmp/mnist_convnet_model")
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)
    train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": train_data}, y=train_labels, batch_size=100, num_epochs=None, shuffle=True)
    mnist_classifier.train(input_fn=train_input_fn, steps=100, hooks=[logging_hook])
    # evaluate
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": eval_data}, y=eval_labels, num_epochs=1, shuffle=False)
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)

if __name__ == "__main__":
    tf.app.run()
