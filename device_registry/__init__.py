from flask import Flask
from flask_restful import Resource, Api
import markdown
import os
from libs.manager.entities import Entities

# Create flask
app = Flask(__name__)
api = Api(app)
entities = Entities()

# Default route
@app.route('/')
def index():
    """
    Default route display documentation
    :return The documentation
    """
    # Open readme file
    with open(os.path.dirname(app.root_path) + "/README.md") as markdown_file:
        content = markdown_file.read()
        # Convert markdown to HTML
        return markdown.markdown(content)


class ProjectList(Resource):

    def get(self):
        projects = entities.get_projects()
        return {'data': projects, 'message': 'Success'}

api.add_resource(ProjectList, '/projects')