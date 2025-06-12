import logging
from datetime import datetime
import os
from django.conf import settings

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        Initialize middleware and setup logger.
        """

        self.get_response = get_response

        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel("DEBUG")

        # Create handlers for console and file logging
        self.console_handler = logging.StreamHandler()
        log_file = os.path.join(settings.BASE_DIR, 'requests.log')
        self.file_handler = logging.FileHandler(log_file)

        # Set the logging level for both handlers
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

        # Create a formatter and set it for both handlers
        self.formatter = logging.Formatter(
            '{levelname} - {message}',
            style='{',
        )
        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter) 

    def __call__(self, request):
        '''any logic you want to add before the requeat 
            reaches the view( or the next middleware in the chian)
        '''
        if hasattr(request, "user") and request.user.is_authenticated:
            self.user = request.user.username
        else:
            self.user = "Anonymous"
        self.logger.debug( f"{datetime.now()} - User: {self.user} - Path: {request.path}")
        response = self.get_response(request)

        '''any logic you want to add
          after the view has returned a response
          '''
        return response