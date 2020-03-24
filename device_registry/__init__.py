from flask import Flask
from flask_restful import Resource, Api, reqparse
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
    """Project manage route"""
    def get(self):
        projects = entities.get_projects()
        return {'data': projects, 'message': 'Success'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name_short', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('disc_path', required=True)
        args = parser.parse_args()
        entities.set_projects(args['name_short'], args['name'], args['disc_path'])
        return {'message': 'Project registered', 'data': args}, 201


api.add_resource(ProjectList, '/projects')