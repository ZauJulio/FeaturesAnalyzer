ModelDocs = """
Model creator

Parameters
----------
    typ: str()
        type of model, [rgs, som, mlp]

    tryLoad: bool()
        Attempt to load model from disk

    db: str(), default="localFile"
        Must be one of the following modes = [direct, localFile]
            direct    -> Use Adapter to direct connection in PostgreSQL server (Fast and Secure)
            localFile -> Save in .csv file (Slow and Less Secure)

        All methods support concurrency, however, the safest is direct with 0% chance of
        problems occurring, followed by localFile with 4.7% and 6x slower.

    dbAcessParms: dict() - If type direct
        dbname: str() the database name
        database: str() the database name (only as keyword argument)
        user: str() user name used to authenticate
        password: str() password used to authenticate
        host: str() database host address (defaults to UNIX socket if not provided)
        port: str() connection port number (defaults to 5432 if not provided)

    Only for regressions:
        degree: int()
            Degree of regression.

        typeRgs: str()
            Must be one of the following types = [linear, ransac, rlm]

    Only for Multilayer Perceptron:
        layers: dict()
            units: int()
            activation: str()

        compile: dict()
            optimizer: str()
            loss: str()
            metrics: list() of str()

        fit: dict()
            batch_size: int() or None
            epochs: int()
            verbose: int(0 or 1 or 2)
            shuffle: bool()
            initial_epoch: int()

        # Layers Arguments
            units: Positive integer, dimensionality of the output space.
            activation: Activation function to use
                If you don't specify anything, no activation is applied
                (ie. "linear" activation: `a(x) = x`).
            use_bias: Boolean, whether the layer uses a bias vector.
            kernel_initializer: Initializer for the `kernel` weights matrix
            bias_initializer: Initializer for the bias vector
            kernel_regularizer: Regularizer function applied to
                the `kernel` weights matrix
            bias_regularizer: Regularizer function applied to the bias vector
            activity_regularizer: Regularizer function applied to
                the output of the layer (its "activation").
            kernel_constraint: Constraint function applied to
                the `kernel` weights matrix
            bias_constraint: Constraint function applied to the bias vector

            # Input shape
                nD tensor with shape: `(batch_size, ..., input_dim)`.
                The most common situation would be
                a 2D input with shape `(batch_size, input_dim)`.

            # Output shape
                nD tensor with shape: `(batch_size, ..., units)`.
                For instance, for a 2D input with shape `(batch_size, input_dim)`,
                the output would have shape `(batch_size, units)`.

        # Compile Arguments
            optimizer: String (name of optimizer) or optimizer instance.
                See [optimizers](/optimizers).
            loss: String (name of objective function) or objective function.
                See [losses](/losses).
                If the model has multiple outputs, you can use a different loss
                on each output by passing a dictionary or a list of losses.
                The loss value that will be minimized by the model
                will then be the sum of all individual losses.
            metrics: List of metrics to be evaluated by the model
                during training and testing.
                Typically you will use `metrics=['accuracy']`.
                To specify different metrics for different outputs of a
                multi-output model, you could also pass a dictionary,
                such as `metrics={'output_a': 'accuracy'}`.
            loss_weights: Optional list or dictionary specifying scalar
                coefficients (Python floats) to weight the loss contributions
                of different model outputs.
                The loss value that will be minimized by the model
                will then be the *weighted sum* of all individual losses,
                weighted by the `loss_weights` coefficients.
                If a list, it is expected to have a 1:1 mapping
                to the model's outputs. If a tensor, it is expected to map
                output names (strings) to scalar coefficients.
            sample_weight_mode: If you need to do timestep-wise
                sample weighting (2D weights), set this to `"temporal"`.
                `None` defaults to sample-wise weights (1D).
                If the model has multiple outputs, you can use a different
                `sample_weight_mode` on each output by passing a
                dictionary or a list of modes.
            weighted_metrics: List of metrics to be evaluated and weighted
                by sample_weight or class_weight during training and testing.
            target_tensors: By default, Keras will create placeholders for the
                model's target, which will be fed with the target data during
                training. If instead you would like to use your own
                target tensors (in turn, Keras will not expect external
                Numpy data for these targets at training time), you
                can specify them via the `target_tensors` argument. It can be
                a single tensor (for a single-output model), a list of tensors,
                or a dict mapping output names to target tensors.

        # Fit Arguments
            x: Numpy array of training data (if the model has a single input),
                or list of Numpy arrays (if the model has multiple inputs).
                If input layers in the model are named, you can also pass a
                dictionary mapping input names to Numpy arrays.
                `x` can be `None` (default) if feeding from
                framework-native tensors (e.g. TensorFlow data tensors).
            y: Numpy array of target (label) data
                (if the model has a single output),
                or list of Numpy arrays (if the model has multiple outputs).
                If output layers in the model are named, you can also pass a
                dictionary mapping output names to Numpy arrays.
                `y` can be `None` (default) if feeding from
                framework-native tensors (e.g. TensorFlow data tensors).
            batch_size: Integer or `None`.
                Number of samples per gradient update.
                If unspecified, `batch_size` will default to 32.
            epochs: Integer. Number of epochs to train the model.
                An epoch is an iteration over the entire `x` and `y`
                data provided.
                Note that in conjunction with `initial_epoch`,
                `epochs` is to be understood as "final epoch".
                The model is not trained for a number of iterations
                given by `epochs`, but merely until the epoch
                of index `epochs` is reached.
            verbose: Integer. 0, 1, or 2. Verbosity mode.
                0 = silent, 1 = progress bar, 2 = one line per epoch.
            callbacks: List of `keras.callbacks.Callback` instances.
                List of callbacks to apply during training.
                See [callbacks](/callbacks).
            validation_split: Float between 0 and 1.
                Fraction of the training data to be used as validation data.
                The model will set apart this fraction of the training data,
                will not train on it, and will evaluate
                the loss and any model metrics
                on this data at the end of each epoch.
                The validation data is selected from the last samples
                in the `x` and `y` data provided, before shuffling.
            validation_data: tuple `(x_val, y_val)` or tuple
                `(x_val, y_val, val_sample_weights)` on which to evaluate
                the loss and any model metrics at the end of each epoch.
                The model will not be trained on this data.
                `validation_data` will override `validation_split`.
            shuffle: Boolean (whether to shuffle the training data
                before each epoch) or str (for 'batch').
                'batch' is a special option for dealing with the
                limitations of HDF5 data; it shuffles in batch-sized chunks.
                Has no effect when `steps_per_epoch` is not `None`.
            class_weight: Optional dictionary mapping class indices (integers)
                to a weight (float) value, used for weighting the loss function
                (during training only).
                This can be useful to tell the model to
                "pay more attention" to samples from
                an under-represented class.
            sample_weight: Optional Numpy array of weights for
                the training samples, used for weighting the loss function
                (during training only). You can either pass a flat (1D)
                Numpy array with the same length as the input samples
                (1:1 mapping between weights and samples),
                or in the case of temporal data,
                you can pass a 2D array with shape
                `(samples, sequence_length)`,
                to apply a different weight to every timestep of every sample.
                In this case you should make sure to specify
                `sample_weight_mode="temporal"` in `compile()`.
            initial_epoch: Integer.
                Epoch at which to start training
                (useful for resuming a previous training run).
            steps_per_epoch: Integer or `None`.
                Total number of steps (batches of samples)
                before declaring one epoch finished and starting the
                next epoch. When training with input tensors such as
                TensorFlow data tensors, the default `None` is equal to
                the number of samples in your dataset divided by
                the batch size, or 1 if that cannot be determined.
            validation_steps: Only relevant if `steps_per_epoch`
                is specified. Total number of steps (batches of samples)
                to validate before stopping.

    Only for Self-Organizing:
        x: int, (default=-1 : Choose an optimized size)
            Number of nodes in X axis

        y: int, (default=-1 : Choose an optimized size)
            Number of nodes in Y axis

        inputLen: int, (default=-1 : Uses the number of columns in the data)
            Number of the elements of the vectors in input

        iterations: int, (default=-1 : Uses the number of samples * the length of the samples)
            Number of iterations

        sigma: float, (default=1.0)
            Spread of the neighborhood function, needs to be adequate
            to the dimensions of the map.
            (at the iteration t we have sigma(t) = sigma / (1 + t/T)
            where T is #num_iteration/2)

        learningRate: float, (default=0.5)
            (at the iteration t we have
            learning_rate(t) = learning_rate / (1 + t/T)
            where T is #num_iteration/2)

        neighborhoodFunction: str, optional (default='gaussian')
            Function that weights the neighborhood of a position in the map.
            Possible values: 'gaussian', 'mexican_hat', 'bubble', 'triangle'

        topology: str, (default='rectangular')
            Topology of the map.
            Possible values: 'rectangular', 'hexagonal'

        activationDistance: str, (default='euclidean')
            Distance used to activate the map.
            Possible values: 'euclidean', 'cosine', 'manhattan', 'chebyshev'

        weightsInit: str, (default='random')
            random: Initializes the weights by randomly sampling data
            pca: Initializes the weightsfrom the two main data components

        randomOrder: bool, optional (default=True)
            Conducts training with random samples or sequentially
"""
