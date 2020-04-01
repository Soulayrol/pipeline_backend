from flask import Flask
from flask_restful import Resource, Api, reqparse
import markdown
import os
from libs.manager.entities import Entities
from spil.libs.sid.sid import Sid
from libs.utils.pipe_exception import PipeException
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

"""
===============================
   Gestion des Asset / Shot
===============================
"""


def get_paths(sid_base):
    try:
        paths = []
        for sid in entities.get_files(sid_base):
            data = sid.data.copy()
            data['id'] = str(sid)
            data['path'] = sid.path
            if sid.has_a("state"):
                info = entities.get_files_info(sid)
                data["date"] = info["date"]
                data["ext"] = info["ext"]
                data["size"] = info["size"]
                data["tag"] = info["tag"]
                data["comment"] = info["comment"]
            paths.append(data)
        return {"data": paths, "message": "Success "}
    except Exception as ex:
        return {"data": False, "message": "Error : " + ex.message}


class FilesFramesList(Resource):
    def get(self, project, type, param1, param2, task, subtask, version, state, frames, ext):
        try:
            return get_paths(Sid(sid='/'.join([project, type, param1, param2, task, subtask, version, state, frames, ext])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}


class FilesExtList(Resource):
    def get(self, project, type, param1, param2, task, subtask, version, state, ext):
        try:
            return get_paths(Sid(sid='/'.join([project, type, param1, param2, task, subtask, version, state, ext])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}

    def post(self, project, type, param1, param2, task, subtask, version, state, ext):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('tag', required=False)
            parser.add_argument('comment', required=False)
            args = parser.parse_args()
            sid = Sid(sid='/'.join([project, type, param1, param2, task, subtask, version, state, ext]))
            entities.create_entity(sid, args['tag'], args['comment'])
            return {'message': "Success", 'data': True}, 201
        except PipeException as ex:
            return {'message': str(ex.message), 'data': False}, 409
        except Exception as ex:
            return {'message': str(ex.message), 'data': False}, 409


class FilesStateList(Resource):
    def get(self, project, type, param1, param2, task, subtask, version, state):
        try:
            return get_paths(Sid(sid='/'.join([project, type, param1, param2, task, subtask, version, state, "*"])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}


class FilesVersionList(Resource):
    def get(self, project, type, param1, param2, task, subtask, version):
        try:
            return get_paths(Sid(sid='/'.join([project, type, param1, param2, task, subtask, version, "*"])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}


class FilesSubtaskList(Resource):
    def get(self, project, type, param1, param2, task, subtask):
        try:
            return get_paths(Sid(sid='/'.join([project, type, param1, param2, task, subtask, "*", "*"])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}


class FilesTaskList(Resource):
    def get(self, project, type, param1, param2, task):
        try:
            return get_paths(Sid(sid='/'.join([project, type, param1, param2, task, "*"])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}


class FilesParam2List(Resource):
    def get(self, project, type, param1, param2):
        try:
            return get_paths(Sid(sid='/'.join([project, type, param1, param2, "*"])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}


class FilesParam1List(Resource):
    def get(self, project, type, param1):
        try:
            return get_paths(Sid(sid='/'.join([project, type, param1, "*"])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}


class FilesTypeList(Resource):
    def get(self, project, type):
        try:
            return get_paths(Sid(sid='/'.join([project, type, "*"])))
        except Exception as ex:
            return {"data": [], "message": "Erreur : " + ex.message}


api.add_resource(FilesFramesList, '/file/<project>/<type>/<param1>/<param2>/<task>/<subtask>/<version>/<state>/<ext>/<frames>')
api.add_resource(FilesExtList, '/file/<project>/<type>/<param1>/<param2>/<task>/<subtask>/<version>/<state>/<ext>')
api.add_resource(FilesStateList, '/file/<project>/<type>/<param1>/<param2>/<task>/<subtask>/<version>/<state>')
api.add_resource(FilesVersionList, '/file/<project>/<type>/<param1>/<param2>/<task>/<subtask>/<version>')
api.add_resource(FilesSubtaskList, '/file/<project>/<type>/<param1>/<param2>/<task>/<subtask>')
api.add_resource(FilesTaskList, '/file/<project>/<type>/<param1>/<param2>/<task>')
api.add_resource(FilesParam2List, '/file/<project>/<type>/<param1>/<param2>')
api.add_resource(FilesParam1List, '/file/<project>/<type>/<param1>')
api.add_resource(FilesTypeList, '/file/<project>/<type>')
