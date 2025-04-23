import tensorflow as tf
from tensorflow.keras import backend
from tensorflow.keras.layers import Layer, Dense, Conv2D

from tensorflow.keras.models import Sequential

# ------------------------------------------------------------------------------------------------------------------


def get_broadcastable_shape(input_shape, axis):

    axis = list(sorted(axis))

    rank = len(input_shape)
    shape = []

    last_axis = 0

    for i in range(len(axis)):

        if axis[i] < 0:

            axis[i] = rank + axis[i]

        # check if axis mismatches the inputs' rank
        assert 0 <= axis[i] < rank, f'axis out of range: [-{rank}, {rank}), axis={axis[i]}'

        for j in range(last_axis, axis[i] - 1):

            shape.append(1)

        shape.append(input_shape[axis[i]])
        last_axis = axis[i]

    for i in range(last_axis, rank - 1):

        shape.append(1)

    return axis, shape


# ------------------------------------------------------------------------------------------------------------------

def global_average_pooling(features, axis, keepdims=True):

    x = tf.math.reduce_mean(features, axis=axis, keepdims=keepdims)

    return x

# ------------------------------------------------------------------------------------------------------------------


def global_linear_pooling(features, axis, keepdims=True):

    epsilon = backend.epsilon()

    t = tf.math.reduce_mean(features, axis=axis, keepdims=True)
    x = tf.math.reduce_sum(features / (t + epsilon), axis=axis, keepdims=keepdims)

    return x

# ------------------------------------------------------------------------------------------------------------------


def global_exponential_pooling(features, axis, keepdims=True):

    t = tf.nn.softmax(features, axis=axis)
    x = tf.math.reduce_sum(t * features, axis=axis, keepdims=keepdims)

    return x

# ------------------------------------------------------------------------------------------------------------------


def global_attention_pooling(features, attention_scores, axis, keepdims=True):

    x = tf.math.reduce_sum(attention_scores * features, axis=axis, keepdims=keepdims)

    return x


# ------------------------------------------------------------------------------------------------------------------

class Squeeze(Layer):

    methods = {'average': global_average_pooling, 'attention': global_attention_pooling}

    def __init__(self, pooling='attention', in_activation='tanh', scores_activation='softmax', axis=None, **kwargs):

        """
            in_activation & out_activation parameters are ignored for pooling != 'attention'
        """

        super().__init__(**kwargs)

        assert pooling in Squeeze.methods, f'pooling={pooling} is not valid'

        if axis is None:

            axis = [1, 2]

        elif isinstance(axis, int):

            axis = [axis]

        self.pooling = pooling
        self.in_activation = in_activation
        self.scores_activation = scores_activation
        self.axis = axis

    def get_config(self):

        cfgs = super().get_config()
        cfgs.update({'pooling': self.pooling, 'axis': self.axis,
                     'in_activation': self.in_activation,
                     'scores_activation': self.scores_activation})

        return cfgs

    # noinspection PyAttributeOutsideInit
    def build(self, input_shape):

        if self.pooling == 'attention':

            fan_out = input_shape[-1]

            self.scores_estimator = Sequential([
                Dense(units=fan_out, activation=self.in_activation, input_shape=input_shape[1:],
                      name=self.name + '_fmap'),
                Dense(units=fan_out, activation=self.scores_activation, name=self.name + '_attn_scores')
            ])

        self.built = True

    def call(self, inputs):

        if self.pooling == 'attention':

            attention_scores = self.scores_estimator(inputs)

            return self.methods[self.pooling](inputs, attention_scores, axis=self.axis)

        return self.methods[self.pooling](inputs, axis=self.axis)

# ------------------------------------------------------------------------------------------------------------------


class Excitation(Layer):

    def __init__(self, decay=0.5, in_activation='relu', out_activation='sigmoid', **kwargs):

        super().__init__(**kwargs)

        assert 0 < decay < 1, 'decay must be in range (0, 1)'

        self.decay = decay
        self.in_activation = in_activation
        self.out_activation = out_activation

    def get_config(self):

        cfgs = super().get_config()
        cfgs.update({'decay': self.decay, 'in_activation': self.in_activation,
                     'out_activation': self.out_activation})

        return cfgs

    # noinspection PyAttributeOutsideInit
    def build(self, input_shape):

        fan_h = int(self.decay * input_shape[-1])
        fan_out = input_shape[-1]

        self.estimator = Sequential([
            Dense(units=fan_h, activation=self.in_activation, name=self.name + '_fmap_a'),
            Dense(units=fan_out, activation=self.out_activation, name=self.name + '_fmap_b')
        ])

        self.built = True

    def call(self, inputs):

        return self.estimator(inputs)

# ------------------------------------------------------------------------------------------------------------------


class SpatialAttention(Layer):

    def __init__(self, decay=0.125, **kwargs):

        super().__init__(**kwargs)

        self.decay = decay

    def get_config(self):

        cfgs = super().get_config()
        cfgs.update({'decay': self.decay})

        return cfgs

    # noinspection PyAttributeOutsideInit
    def build(self, input_shape):

        rank = len(input_shape)

        assert rank == 4, f'Expected 4d inputs (NHWC), but found {rank}d ones'

        fan_h = int(self.decay * input_shape[-1])
        fan_out = input_shape[-1]

        # {query_estimator --> B, key_estimator --> C, value_estimator --> D}
        self.query_estimator = Conv2D(filters=fan_h, kernel_size=(1, 1), use_bias=False,
                                      name=self.name + '_query_estimator', input_shape=input_shape[1:])

        self.key_estimator = Conv2D(filters=fan_h, kernel_size=(1, 1), use_bias=False,
                                    name=self.name + '_key_estimator', input_shape=input_shape[1:])

        self.value_estimator = Conv2D(filters=fan_out, kernel_size=(1, 1), use_bias=False,
                                      name=self.name + '_value_estimator', input_shape=input_shape[1:])

        self.alpha = self.add_weight(shape=(fan_out, ), initializer='ones', trainable=True, name='alpha')
        self.built = True

    def call(self, inputs):

        query = self.query_estimator(inputs)
        key = self.key_estimator(inputs)
        value = self.value_estimator(inputs)

        # N(HW)(HW) - 5D tensor
        scores = tf.einsum('bijk,bxyk->bijxy', query, key)
        scores = tf.keras.activations.softmax(scores, axis=[3, 4])

        # NHWC - 4D tensor (of shape same as inputs)
        outputs = tf.einsum('bijxy,bxyk->bijk', scores, value)
        outputs = self.alpha * outputs + inputs

        return outputs

# ------------------------------------------------------------------------------------------------------------------


class ChannelAttention(Layer):

    """
        similar to self-attention
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def get_config(self):

        cfgs = super().get_config()

        return cfgs

    # noinspection PyAttributeOutsideInit
    def build(self, input_shape):

        rank = len(input_shape)

        assert rank == 4, f'Expected 4d inputs (NHWC), but found {rank}d ones'

        fan_out = input_shape[-1]

        self.beta = self.add_weight(shape=(fan_out, ), initializer='ones', trainable=True, name='beta')
        self.built = True

    def call(self, inputs):

        # N(C)(C) - 3D tensor
        scores = tf.einsum('bijk,bjil->bkl', inputs, inputs)
        scores = tf.keras.activations.softmax(scores, axis=[2])

        # NHWC - 4D tensor (of shape same as inputs)
        outputs = tf.einsum('bij,bkli->bklj', scores, inputs)
        outputs = self.beta * outputs + inputs

        return outputs

# ------------------------------------------------------------------------------------------------------------------
