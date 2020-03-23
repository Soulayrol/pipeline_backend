from engine import Engine
import os
import hou
import time
from spil.libs.sid.sid import Sid
from utils import log

class HoudiniEngine(Engine):

    def open(self, path):
        """
        Open file
        """
        hou.hipFile.load(path, suppress_save_prompt=True)
        # self.set_env_var(path)

    def set_env_var(self, path):
        """
        Workspace
        """
        workspace_path = path.split('/scenes')[0]
        pnum = ''
        snum = ''
        name = ''
        if '02_SHOT' in path.split('/'):        # FIXME: redo with sid.
            shot_path = path.split('02_SHOT')[0] + '02_SHOT/3d'
            asset_path = path.split('02_SHOT')[0] + '01_ASSET_3D'
            pnum = path.split('/')[8]
            snum = path.split('/')[7]
            wipcache_path = os.path.join(path.split('02_SHOT/3d/scenes')[0],
                                         '03_WIP_CACHE_FX', pnum, snum).replace(os.sep, '/')
            pubcache_path = os.path.join(path.split('02_SHOT/3d/scenes')[0],
                                         '04_PUBLISH_CACHE_FX', pnum, snum).replace(os.sep, '/')
        else:
            shot_path = path.split('01_ASSET_3D')[0] + '02_SHOT/3d'
            asset_path = path.split('01_ASSET_3D')[0] + '01_ASSET_3D'
            name = path.split('/')[6]
            wipcache_path = os.path.join(path.split('01_ASSET_3D')[
                                         0], '03_WIP_CACHE_FX', name).replace(os.sep, '/')
            pubcache_path = os.path.join(path.split('01_ASSET_3D')[
                                         0], '04_PUBLISH_CACHE_FX', name).replace(os.sep, '/')

        sid = Sid(path=path)

        if sid.is_shot():
            farm = '{}_{}_{}'.format(sid.get('project').upper(), sid.get('seq'), sid.get('shot'))
        elif sid.is_asset():
            farm = '{}_{}'.format(sid.get('project').upper(), sid.get('name'))

        project = sid.get_as('project').path
        images_out = os.path.dirname(sid.get_with(ext='exr').path)

        envs = {
            'JOB': workspace_path,
            'WIPCACHE': wipcache_path,
            'PUBCACHE': pubcache_path,
            'ASSET': asset_path,
            'SHOT': shot_path,
            'PNUM': pnum,       # would call SHOT_PATH for path and SHOT for the shot
            'SNUM': snum,
            'ASSET_NAME': name,
            'FARM': farm,
            'PROJECT': project,
            'SID': str(sid),
            'IMAGES_OUT': images_out,
        }

        for key, value in envs.iteritems():
            hou.hscript('setenv {}={}'.format(key, value))
            log.debug('${} = {}'.format(key, value))

        log.debug('Done set_env_var')

    def open_as(self, path):
        """
        Open file and rename it with a time value
        for keep the source file
        """
        path = self.conform(path)
        hou.hipFile.load(path, suppress_save_prompt=True)
        hou.hipFile.setName(path.replace(
            ".hipnc", "_{}.hipnc".format(time.time())))

    def save(self, path):
        """
        Save file as path
        """
        path = self.conform(path)
        hou.hipFile.save(path)

    def get_file_path(self):
        """
        Get the current file path (from the current open file)
        """
        return hou.hipFile.path()

    def set_workspace(self, path):
        """
        Set the workspace
        """
        path = self.conform(path)
        os.environ["JOB"] = path
        hou.allowEnvironmentToOverwriteVariable("JOB", True)

    def __str__(self):
        return 'houdini'


if __name__ == '__main__':
    """
    Test
    """
    # Create engine
    engine = HoudiniEngine()
    print("Engine : " + str(engine))
    # Get engine path
    print("Current file location : " + engine.get_file_path())
    # Save
    engine.save(r"C:\Users\Sylvain\Desktop\test" + engine.get_ext())
    print("Current file location after save : " + engine.get_file_path())
    # Open as
    engine.open_as(engine.get_file_path())
    print("Open as ")
    print("Current file location after open as : " + engine.get_file_path())
    engine.save(engine.get_file_path())
    # Open
    engine.open(r"C:\Users\Sylvain\Desktop\test" + engine.get_ext())
    print("Current file location after open : " + engine.get_file_path())
