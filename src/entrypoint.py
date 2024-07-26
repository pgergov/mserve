from .app import create_app
from .serve import create_handles


handles = create_handles()
app = create_app(**handles)
