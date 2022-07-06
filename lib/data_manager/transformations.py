from sklearn.preprocessing import (MaxAbsScaler, MinMaxScaler, Normalizer,
                                   RobustScaler, StandardScaler, PolynomialFeatures,
                                   Binarizer, QuantileTransformer, PowerTransformer)


class Transform:
    def __init__(self):
        """  """
        self.__scaler = {}
        self.parms = {}
        self.transformations = {
            "Normalize": self.normalize,
            "Standardize": self.standardize,
            "MinMax": self.min_max,
            "MaxAbs": self.max_abs,
            "Robust": self.robust,
            "Binarizer": self.binarizer,
            "Quantile": self.quantile,
            "Power": self.power,
        }

    def normalize(self, norm='l2', inplace=True):
        """ Normalize samples individually to unit norm.

        Normalize samples individually to unit norm.

        Parameters
        ----------
        norm : str()
            ‘l1’, ‘l2’, or ‘max’, optional (‘l2’ by default)
            The norm to use to normalize each non zero sample.

        inplace : bool()
            Saves the variable in the attribute of the current instance.
        """
        self.df = self.df.ffill()
        self.df = self.df.bfill()
        self.__scaler['norm'] = Normalizer(norm=norm)
        self.__scaler['norm'].fit(self.df.values)
        if inplace:
            self.parms['norm'] = [norm]
            self.df = self.reindex(
                self.__scaler['norm'].transform(self.df.values))
            return self.df
        return self.reindex(self.__scaler['norm'].transform(self.df.values))

    def standardize(self, with_mean=True, with_std=True, inplace=True):
        """ Standardize features by removing the mean and scaling to unit variance

        Computes the standardization using the z-score = (x - μ) / σ, where:
        x is a score
        σ is the population standard deviation
        μ is the population mean

        Parameters
        ----------
        with_mean : boolean, True by default
            If True, center the array before scaling. This does not work
            (and will raise an exception) when attempted on sparse matrices,
            because centering them entails building a dense matrix which in
            common use cases is likely to be too large to fit in memory.

        with_std : boolean, True by default
            If True, scale the array to unit variance (or equivalently, unit
            standard deviation).

        inplace : bool()
            Saves the variable in the attribute of the current instance.
        """
        self.__scaler['std'] = StandardScaler(with_mean=with_mean, with_std=with_std)
        self.__scaler['std'].fit(self.df.values)
        if inplace:
            self.parms['std'] = [with_mean, with_std]
            self.df = self.reindex(
                self.__scaler['std'].transform(self.df.values))
            return self.df
        return self.reindex(self.__scaler['std'].transform(self.df.values))

    def min_max(self, feature_range=(0, 1), inplace=True):
        """ Transform features by scaling each feature to a given range.

        Transform features by scaling each feature to a given range.

        This estimator scales and translates each feature individually
        such that it is in the given range on the training set, e.g.
        between zero and one.

        Parameters
        ----------
        feature_range : tuple(min, max)
                Desired range of transformed data.
                default : (0, 1)

        inplace : bool()
            Saves the variable in the attribute of the current instance.
        """
        self.__scaler['min_max'] = MinMaxScaler(feature_range=feature_range)
        self.__scaler['min_max'].fit(self.df.values)
        if inplace:
            self.parms['min_max'] = [feature_range]
            self.df = self.reindex(
                self.__scaler['min_max'].transform(self.df.values))
            return self.df
        return self.reindex(self.__scaler['min_max'].transform(self.df.values))

    def max_abs(self, inplace=True):
        """Scale each feature by its maximum absolute value.

        This estimator scales and translates each feature individually such
        that the maximal absolute value of each feature in the
        training set will be 1.0. It does not shift/center the data, and
        thus does not destroy any sparsity.

        This scaler can also be applied to sparse CSR or CSC matrices.


        Parameters
        ----------
        inplace : bool()
            Saves the variable in the attribute of the current instance.
        """
        self.__scaler['max_abs'] = MaxAbsScaler()
        self.__scaler['max_abs'].fit(self.df.values)
        if inplace:
            self.parms['max_abs'] = []
            self.df = self.reindex(
                self.__scaler['max_abs'].transform(self.df.values))
            return self.df
        return self.reindex(self.__scaler['max_abs'].transform(self.df.values))

    def robust(self, with_centering=True, with_scaling=True,
                      quantile_range=(25.0, 75.0), inplace=True):
        """Scale features using statistics that are robust to outliers.

        This Scaler removes the median and scales the data according to
        the quantile range (defaults to IQR: Interquartile Range).
        The IQR is the range between the 1st quartile (25th quantile)
        and the 3rd quartile (75th quantile).

        Centering and scaling happen independently on each feature by
        computing the relevant statistics on the samples in the training
        set. Median and interquartile range are then stored to be used on
        later data using the ``transform`` method.

        Standardization of a dataset is a common requirement for many
        machine learning estimators. Typically this is done by removing the mean
        and scaling to unit variance. However, outliers can often influence the
        sample mean / variance in a negative way. In such cases, the median and
        the interquartile range often give better results.


        Parameters
        ----------
        with_centering : boolean, True by default
            If True, center the data before scaling.
            This will cause ``transform`` to raise an exception when attempted on
            sparse matrices, because centering them entails building a dense
            matrix which in common use cases is likely to be too large to fit in
            memory.

        with_scaling : boolean, True by default
            If True, scale the data to interquartile range.

        quantile_range : tuple (q_min, q_max), 0.0 < q_min < q_max < 100.0
            Default: (25.0, 75.0) = (1st quantile, 3rd quantile) = IQR
            Quantile range used to calculate ``scale_``.

        inplace : bool()
            Saves the variable in the attribute of the current instance.
        """
        self.__scaler['robust'] = RobustScaler(with_centering=with_centering,
                                               with_scaling=with_scaling,
                                               quantile_range=quantile_range)
        self.__scaler['robust'].fit(self.df.values)
        if inplace:
            self.parms['robust'] = [
                                    with_centering,
                                    with_scaling,
                                    quantile_range]
            self.df = self.reindex(
                self.__scaler['robust'].transform(self.df.values))
            return self.df
        return self.reindex(self.__scaler['robust'].transform(self.df.values))

    def binarizer(self, threshold=0.0, inplace=True):
        """Binarize data (set feature values to 0 or 1) according to a threshold

        Values greater than the threshold map to 1, while values less than
        or equal to the threshold map to 0. With the default threshold of 0,
        only positive values map to 1.

        Binarization is a common operation on text count data where the
        analyst can decide to only consider the presence or absence of a
        feature rather than a quantified number of occurrences for instance.

        It can also be used as a pre-processing step for estimators that
        consider boolean random variables (e.g. modelled using the Bernoulli
        distribution in a Bayesian setting).

        Parameters
        ----------
        threshold : float, optional (0.0 by default)
            Feature values below or equal to this are replaced by 0, above it by 1.
            Threshold may not be less than 0 for operations on sparse matrices.

        inplace : bool()
            Saves the variable in the attribute of the current instance.
        """
        self.__scaler['bin'] = Binarizer(threshold=threshold)
        self.__scaler['bin'].fit(self.df.values)
        if inplace:
            self.parms['bin'] = [threshold]
            self.df = self.reindex(
                self.__scaler['bin'].transform(self.df.values))
            return self.df
        return self.reindex(self.__scaler['bin'].transform(self.df.values))

    def quantile(self, n_quantiles=1000, output_distribution='uniform',
                             ignore_implicit_zeros=False, subsample=1e5,
                             random_state=None, inplace=True):
        """Transform features using quantiles information.

        This method transforms the features to follow a uniform or a normal
        distribution. Therefore, for a given feature, this transformation tends
        to spread out the most frequent values. It also reduces the impact of
        (marginal) outliers: this is therefore a robust preprocessing scheme.

        The transformation is applied on each feature independently. First an
        estimate of the cumulative distribution function of a feature is
        used to map the original values to a uniform distribution. The obtained
        values are then mapped to the desired output distribution using the
        associated quantile function. Features values of new/unseen data that fall
        below or above the fitted range will be mapped to the bounds of the output
        distribution. Note that this transform is non-linear. It may distort linear
        correlations between variables measured at the same scale but renders
        variables measured at different scales more directly comparable.


        Parameters
        ----------
        n_quantiles : int, optional (default=1000 or n_samples)
            Number of quantiles to be computed. It corresponds to the number
            of landmarks used to discretize the cumulative distribution function.
            If n_quantiles is larger than the number of samples, n_quantiles is set
            to the number of samples as a larger number of quantiles does not give
            a better approximation of the cumulative distribution function
            estimator.

        output_distribution : str, optional (default='uniform')
            Marginal distribution for the transformed data. The choices are
            'uniform' (default) or 'normal'.

        ignore_implicit_zeros : bool, optional (default=False)
            Only applies to sparse matrices. If True, the sparse entries of the
            matrix are discarded to compute the quantile statistics. If False,
            these entries are treated as zeros.

        subsample : int, optional (default=1e5)
            Maximum number of samples used to estimate the quantiles for
            computational efficiency. Note that the subsampling procedure may
            differ for value-identical sparse and dense matrices.

        random_state : int, RandomState instance or None, optional (default=None)
            If int, random_state is the seed used by the random number generator;
            If RandomState instance, random_state is the random number generator;
            If None, the random number generator is the RandomState instance used
            by np.random. Note that this is used by subsampling and smoothing
            noise.

        inplace : bool()
            Saves the variable in the attribute of the current instance.
        """
        self.__scaler['quantile'] = QuantileTransformer(n_quantiles=n_quantiles,
                                                        output_distribution=output_distribution,
                                                        ignore_implicit_zeros=ignore_implicit_zeros,
                                                        subsample=subsample,
                                                        random_state=random_state)
        self.__scaler['quantile'].fit(self.df.values)
        if inplace:
            self.parms['quantile'] = [n_quantiles,
                                      output_distribution,
                                      ignore_implicit_zeros,
                                      subsample,
                                      random_state]
            self.df = self.reindex(
                self.__scaler['quantile'].transform(self.df.values))
            return self.df
        return self.reindex(self.__scaler['quantile'].transform(self.df.values))

    def power(self, method='yeo-johnson', inplace=True):
        """Apply a power transform featurewise to make data more Gaussian-like.

        Power transforms are a family of parametric, monotonic transformations
        that are applied to make data more Gaussian-like. This is useful for
        modeling issues related to heteroscedasticity (non-constant variance),
        or other situations where normality is desired.

        Currently, PowerTransformer supports the Box-Cox transform and the
        Yeo-Johnson transform. The optimal parameter for stabilizing variance and
        minimizing skewness is estimated through maximum likelihood.

        Box-Cox requires input data to be strictly positive, while Yeo-Johnson
        supports both positive or negative data.

        By default, zero-mean, unit-variance normalization is applied to the
        transformed data.

        Parameters
        ----------
        method : str, (default='yeo-johnson')
            The power transform method. Available methods are:

            - 'yeo-johnson' [1]_, works with positive and negative values
            - 'box-cox' [2]_, only works with strictly positive values

        standardize : boolean, default=True
            Set to True to apply zero-mean, unit-variance normalization to the
            transformed output.

        inplace : bool()
            Saves the variable in the attribute of the current instance.
        """
        self.__scaler['power'] = PowerTransformer(method=method)
        self.__scaler['power'].fit(self.df.values)
        if inplace:
            self.parms['power'] = [method]
            self.df = self.reindex(
                self.__scaler['power'].transform(self.df.values))
            return self.df
        return self.reindex(self.__scaler['power'].transform(self.df.values))

    def get_inverse(self, x, typ):
        """  """
        return self.__scaler[typ].inverse_transform(x)
