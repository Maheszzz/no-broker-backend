"""Custom exception classes for standardized error responses."""
from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "not_found",
                "message": f"{resource} with ID {resource_id} not found"
            }
        )


class DatabaseError(HTTPException):
    """Raised when a database operation fails."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "database_error",
                "message": message
            }
        )


class ValidationError(HTTPException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "validation_error",
                "message": message
            }
        )
