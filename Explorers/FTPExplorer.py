import ExplorerNodes, EditorModels, Utils
import string, os
from wxPython.wx import wxMenu, EVT_MENU, wxMessageBox, wxPlatform
from ZopeLib.ZopeFTP import ZopeFTP
import ftplib

true = 1
false = 0

class FTPController(ExplorerNodes.Controller, ExplorerNodes.ClipboardControllerMix):
    def __init__(self, editor, list):
        ExplorerNodes.ClipboardControllerMix.__init__(self)
        ExplorerNodes.Controller.__init__(self, editor)

        self.list = list
        self.menu = wxMenu()

        self.setupMenu(self.menu, self.list, self.clipMenuDef)
        self.toolbarMenus = [self.clipMenuDef]


class FTPCatNode(ExplorerNodes.CategoryNode):
    defName = 'FTP'
    defaultStruct = {'username': 'anonymous',
                     'passwd': '',
                     'host': 'localhost',
                     'port': 21,
                     'path': '/',
                     'passive': 0}
    def __init__(self, clipboard, config, parent):
        ExplorerNodes.CategoryNode.__init__(self, 'FTP', ('explorer', 'ftp'),
              clipboard, config, parent)

    def createParentNode(self):
        return self

    def createChildNode(self, name, props):
        return FTPConnectionNode(name, props, self.clipboard, self)

    def createCatCompanion(self, catNode):
        comp = ExplorerNodes.CategoryDictCompanion(catNode.treename, self)
        return comp

class FTPItemNode(ExplorerNodes.ExplorerNode):
    protocol = 'ftp'
    def __init__(self, name, props, resourcepath, clipboard, isFolder, imgIdx, parent, ftpConn, ftpObj, root):
        ExplorerNodes.ExplorerNode.__init__(self, name, resourcepath, clipboard, imgIdx,
              parent, props)
        self.isFolder = isFolder
        self.ftpConn = ftpConn
        self.ftpObj = ftpObj
        self.root = root
        self.cache = {}

    def destroy(self):
        self.cache = {}

    def isFolderish(self):
        return self.ftpObj.isFolder()

    def createChildNode(self, obj, root):
        item = FTPItemNode(obj.name, self.properties, self.resourcepath+'/'+obj.name,
              self.clipboard, false, -1 , self, self.ftpConn, obj, root)
        if item.isFolderish():
            item.imgIdx = EditorModels.FolderModel.imgIdx
        else:
            item.imgIdx = EditorModels.TextModel.imgIdx
        return item

    def openList(self, root = None):
        try:
            items = self.ftpConn.dir(self.ftpObj.whole_name())
        except ftplib.error_perm, resp:
            Utils.ShowMessage(None, 'FTP Error', str(resp))
            raise

        if not root: root = self.root
        self.cache = {}
        result = []
        for obj in items:
            if obj.name in ('', '.', '..'):
                continue
            z = self.createChildNode(obj, self.root)
            if z:
                result.append(z)
                self.cache[obj.name] = z

        return result

    def deleteItems(self, names):
        for item in names:
            self.ftpConn.delete(self.cache[item].ftpObj)

    def renameItem(self, name, newName):
        self.ftpConn.rename(self.cache[name].ftpObj, newName)

class FTPConnectionNode(FTPItemNode):
    def __init__(self, name, properties, clipboard, parent):
        ftpConn = ZopeFTP()
        ftpObj = ftpConn.folder_item(os.path.dirname(properties['path']),
                                     os.path.basename(properties['path']))
        FTPItemNode.__init__(self, ftpObj.name, properties, ftpObj.path, clipboard, true,
            EditorModels.imgFSDrive, parent, ftpConn, ftpObj, self)
        self.connected = false
        self.treename = name

    def openList(self):
        if not self.connected:
            try:
                props = self.properties
                self.ftpConn.connect(props['username'], props['passwd'],
                                     props['host'], props['port'],
                                     props['passive'])
            except Exception, message:
                wxMessageBox(`message.args`, 'Error on connect')
                raise
        return FTPItemNode.openList(self, self)

class FTPExpClipboard(ExplorerNodes.ExplorerClipboard):
    def pasteFileSysFolder(self, folderpath, nodepath, ftpConn):
        ftpConn.add_folder(os.path.basename(folderpath), nodepath)
        files = os.listdir(folderpath)
        folder = os.path.basename(folderpath)
        newNodepath = nodepath+'/'+folder
        for file in files:
            file = os.path.join(folderpath, file)
            if os.path.isdir(file):
                self.pasteFileSysFolder(file, newNodepath, zopeConn)
            else:
                ftpConn.upload(file, newNodepath)

    def clipPaste_FileSysExpClipboard(self, node, nodes, mode):
        nodepath = node.resourcepath
        for file in nodes:
            if file.isDir():
                self.pasteFileSysFolder(file.resourcepath, nodepath, node.ftpConn)
            else:
                node.ftpConn.upload(file.resourcepath, nodepath)