import os
import numpy as np
import tensorflow as tf
import sys



# Load them!
cwd = os.getcwd()
loadpath = cwd + "/../custom_data_signs.npz"
l = np.load(loadpath)

# See what's in here
print (l.files)

# Parse data
trainimg = l['trainimg']
trainlabel = l['trainlabel']
testimg = l['testimg']
testlabel = l['testlabel']
imgsize = l['imgsize']
use_gray = l['use_gray']
ntrain = trainimg.shape[0]
nclass = trainlabel.shape[1]
dim    = trainimg.shape[1]
ntest  = testimg.shape[0]
print ("%d train images loaded" % (ntrain))
print ("%d test images loaded" % (ntest))
print ("%d dimensional input" % (dim))
print ("Image size is %s" % (imgsize))
print ("%d classes" % (nclass))


#define variables
tf.set_random_seed(0)
n_input  = dim
n_output = nclass
if use_gray:
    weights  = {
        'wd1': tf.Variable(tf.random_normal(
                [(int)(imgsize[0]*imgsize[1]), 128], stddev=0.1),name="wd1"),
        'wd2': tf.Variable(tf.random_normal([128, n_output], stddev=0.1),name="wd2")
    }
else:
    print "You should use gray images!!"
    
biases   = {
    'bd1': tf.Variable(tf.random_normal([128], stddev=0.1),name="bd1"),
    'bd2': tf.Variable(tf.random_normal([n_output], stddev=0.1),name="bd2")
}

#define network
def conv_basic(_input, _w, _b, _keepratio, _use_gray):
    # INPUT
    if _use_gray:
        _input_r = tf.reshape(_input, shape=[-1, imgsize[0], imgsize[1], 1])
    else:
        _input_r = tf.reshape(_input, shape=[-1, imgsize[0], imgsize[1], 3])
    # VECTORIZE
    _dense1 = tf.reshape(_input_r
                         , [-1, _w['wd1'].get_shape().as_list()[0]])
    # FULLY CONNECTED LAYER 1
    _fc1 = tf.nn.relu(tf.add(tf.matmul(_dense1, _w['wd1']), _b['bd1']))
    _fc_dr1 = tf.nn.dropout(_fc1, _keepratio)
    # FULLY CONNECTED LAYER 2
    _out = tf.add(tf.matmul(_fc_dr1, _w['wd2']), _b['bd2'])
    # RETURN
    out = {
        'out': _out
    }
    return out
print ("NETWORK READY")




