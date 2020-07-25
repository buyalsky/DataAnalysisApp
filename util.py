def unstable_node(inner_class):
    def not_implemented_func(*args, **kwargs):
        raise NotImplementedError
    inner_class.run = not_implemented_func
    return inner_class
