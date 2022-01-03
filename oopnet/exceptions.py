class ComponentExistsError(Exception):
    """Raised when a component with the same ID already exists in the network."""
    def __init__(self, id, message=None):
        if not message:
            self.message = f'A component with the ID "{id}" already exists in the network.'
        super().__init__(self.message)