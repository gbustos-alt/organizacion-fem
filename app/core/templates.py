from fastapi.templating import Jinja2Templates

# Global templates instance pointing to the templates directory
templates = Jinja2Templates(directory="app/templates")
