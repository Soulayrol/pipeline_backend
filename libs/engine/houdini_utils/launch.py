import hou
import os

here = os.path.dirname(__file__)


def load_shelves():
    # print "Here : ", here
    shelf_dir = os.path.join(here, 'shelves')
    try:
        from pathlib2 import Path
        for shelf_path in Path(shelf_dir).iterdir():
            shelf_path = str(shelf_path).replace(os.sep, r'/')
            # print shelf_path
            shelf_name = os.path.basename(shelf_path).split('.')[0]
            if shelf_name not in hou.shelves.shelfSets():
                hou.shelves.loadFile(shelf_path)
                print('Loaded shelf : {}'.format(shelf_name))

    except Exception as e:
        print('Problem loading Pipeline shelves')
        print(e)
