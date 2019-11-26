
def create_registrar():
    registry = {}

    def registrar(func):
        registry[func.__name__] = func
        return func
    registrar.all = registry
    return registrar
