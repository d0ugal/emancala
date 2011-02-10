
class _DjangoException(Exception):
    
    def __unicode__(self):
        """
        Added __unicode__ for working with Django nicely.
        """
        return self.__str__()

class InvalidMoveError(_DjangoException):
    """
    Custom exception for use when dealing with bogus moves
    """

class TurnNotFinishedError(_DjangoException):
    """
    Custom exception for use when dealing with bogus moves
    """

class ImproperlyConfiguredError(_DjangoException):
    """
    Custom exception for use when dealing with configuration/setup errors
    """