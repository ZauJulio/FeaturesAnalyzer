DBAcessModeError = ValueError("""
    Database acess mode must be either direct, sio or localfile
""")


InvalidModelTypeError = ValueError("""
    Invalid model type. It must be one of the following:
        [som, mlp, rgs]
""")


InvalidRegressionTypeError = ValueError("""
    Invalid regression type. It must be one of the following:
        [linear, ransac, rlm]
""")


InvalidTableName = ValueError("""
    Invalid table name. It must be one of the following:
        [data, som, mlp, rgs]
""")

InvalidDBOptions = ValueError("""
    Invalid db type. It must be one of the following:
        [sqlite, postgres]
""")