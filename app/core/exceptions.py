class DomainError(Exception):
    """ Base class for all domain-related errors. """
    pass

class UserAlreadyExists(DomainError):
    def __init__(self, email: str):
        self.email = email
        
        message = f'User with email "{email}" already exists'
        super().__init__(message)