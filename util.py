def unstable_node(inner_class):
    def not_implemented(*args, **kwargs):
        raise NotImplementedError
    inner_class.run = not_implemented
    return inner_class
