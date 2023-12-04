""" Main entry point of the application.
    
    Imports necessary controllers and starts the server to run the application.
"""

from controllers.data import *
from controllers.display import *
from controllers.event import *
from controllers.login import *
from controllers.search import *
from server.instance import server

if __name__ == "__main__":
    server.run(debug=True)
