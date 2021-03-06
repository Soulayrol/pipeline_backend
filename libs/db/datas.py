from libs.db.FS.file_system import FileSystem
from libs.db.cgw.cgwire import CgWire
from spil.libs.sid.sid import Sid
from libs.utils import pipe_exception as pe
from libs.utils import log
import conf


class Datas(object):

    def __init__(self):
        self.file_system = FileSystem()
        self.cgw = CgWire()

    # region File System
    """
    =============
       FS DATA
    =============
    """
    def get(self, sid):
        """
        Glob one
        :return: The list
        """
        try:
            return self.file_system.get(sid)
        except Exception as ex:
            raise ex

    def create_path(self, path):
        """Create a file system path"""
        return self.file_system.create_path(path)

    def get_next_version(self, sid):
        """
        Get the sid of the new version
        :return: the sid of the new version
        """
        return self.file_system.get_next_version(sid)

    def make_new_version(self, sid, tag, comment):
        """
        This function create a new directory af the max version and return the path
        Create a json with description
        :return The new sid
        """
        return self.file_system.make_new_version(sid, tag, comment)

    def get_projects(self):
        """
        Get the list of projects
        :return: the list of projects
        """
        return conf.projects

    def create_entity(self, sid, tag='', comment=''):  # TODO pass a entity object
        """
        Create entity
        """
        try:
            if sid.is_asset():
                sid = self.file_system.create_asset(sid, tag, comment)
                return sid
            else:
                sid = self.file_system.create_shot(sid, tag, comment)
                return sid
        except Exception as ex:
            raise ex

    def conform_entity(self, sid):  # TODO pass a entity object
        """
        Conform entity
        """
        if sid.is_asset():
            return self.file_system.conform_asset(sid)
        else:
            return self.file_system.conform_shot(sid)

    def get_file_info(self, sid):
        try:
            sid = sid.get_as("state")
            coment = self.file_system.get_comment(sid)
            ext = self.file_system.get_extension(sid)
            tag = self.file_system.get_tag(sid)
            size = self.file_system.get_size(sid)
            date = self.file_system.get_date(sid)
            return {"date": date, "size": size, "tag": tag, "ext": ext, "comment": coment}
        except Exception as ex:
            raise ex

    # endregion


if __name__ == '__main__':

    Datas.create_folders('c:/', ['folder1', 'folder2'])