#-----------------------------------------------------------------------------
# Name:        AppViews.py
# Purpose:     Views for application management
#
# Author:      Riaan Booysen
#
# Created:
# RCS-ID:      $Id$
# Copyright:   (c) 1999 - 2003 Riaan Booysen
# Licence:     GPL
#-----------------------------------------------------------------------------
print 'importing Views.AppViews'

""" View classes for the AppModel """

from os import path
import time

try:
    from cmp import cmp
except ImportError:
    from filecmp import cmp

from wxPython.wx import *

from EditorViews import ListCtrlView, ModuleDocView, wxwAppModuleTemplate, CloseableViewMix
import SourceViews
import Search, Utils

class AppFindResults(ListCtrlView, CloseableViewMix):
    gotoLineBmp = 'Images/Editor/GotoLine.png'

    viewName = 'Application Find Results'
    def __init__(self, parent, model):
        CloseableViewMix.__init__(self, 'find results')
        ListCtrlView.__init__(self, parent, model, wxLC_REPORT,
          ( ('Goto match', self.OnGoto, self.gotoLineBmp, ''),
            ('Rerun query', self.OnRerun, '-', ''),
          ) +
            self.closingActionItems, 0)

        self.InsertColumn(0, 'Module', width = 100)
        self.InsertColumn(1, 'Line no', wxLIST_FORMAT_CENTRE, 40)
        self.InsertColumn(2, 'Col', wxLIST_FORMAT_CENTRE, 40)
        self.InsertColumn(3, 'Text', width = 550)

        self.results = {}
        self.listResultIdxs = []
        self.tabName = 'Results'
        self.findPattern = ''
        self.active = true
        self.model = model

    def refreshCtrl(self):
        ListCtrlView.refreshCtrl(self)
        i = 0
        self.listResultIdxs = []
        for mod in self.results.keys():
            for result in self.results[mod]:
                self.listResultIdxs.append((mod, result))
                i = self.addReportItems(i, (path.basename(mod), `result[0]`,
                  `result[1]`, result[2].strip()) )

        self.model.editor.statusBar.setHint('%d matches of "%s".'%(i, self.findPattern))

        self.pastelise()

    def OnGoto(self, event):
        if self.selected >= 0:
            modName = self.listResultIdxs[self.selected][0]
            model, cntrl = self.model.openModule(modName)
            srcView = model.views['Source']
            srcView.focus()
            foundInfo = self.listResultIdxs[self.selected][1]
            srcView.lastSearchPattern = self.findPattern
            srcView.lastSearchResults = self.results[modName]
            try:
                srcView.lastMatchPosition = self.results[modName].index(foundInfo)
            except:
                srcView.lastMatchPosition = 0
                print 'foundInfo not found'

            srcView.selectSection(foundInfo[0], foundInfo[1], self.findPattern)

    def OnRerun(self, event):
        self.rerun(None)

# XXX Add 'Get description from module info' option
class AppView(ListCtrlView):
    openBmp = 'Images/Editor/OpenFromApp.png'
    addModBmp = 'Images/Editor/AddToApp.png'
    remModBmp = 'Images/Editor/RemoveFromApp.png'
    findBmp = 'Images/Shared/Find.png'

    viewName = 'Application'
    def __init__(self, parent, model):
        ListCtrlView.__init__(self, parent, model, wxLC_REPORT,
          (('Open', self.OnOpen, self.openBmp, ''),
           ('-', None, '', ''),
           ('Add', self.OnAdd, self.addModBmp, 'Insert'),
           ('Edit', self.OnEdit, '-', ''),
           ('Remove', self.OnRemove, self.remModBmp, 'Delete'),
           ('-', None, '', ''),
           ('Find', self.OnFind, self.findBmp, 'Find'),
           ('-', None, '-', ''),
           ('Make module main module', self.OnMakeMain, '-', ''),
           ), 0)

        self.InsertColumn(0, 'Module', width = 150)
        self.InsertColumn(1, 'Type', width = 50)
#        self.InsertColumn(2, 'Autocreate', wxLIST_FORMAT_CENTRE, 50)
        self.InsertColumn(2, 'Description', width = 150)
        self.InsertColumn(3, 'Relative path', width = 220)

        self.sortOnColumns = [0, 1, 3]

#        EVT_LIST_BEGIN_DRAG(self, self.GetId(), self.OnDrag)

        self.SetImageList(model.editor.modelImageList, wxIMAGE_LIST_SMALL)

        self.lastSearchPattern = ''
        self.active = true
        self.canExplore = true
        self.model = model

    def OnDrag(self, event):
        print 'drag', event.GetString()
        print 'drag', dir(event.__class__.__bases__[0])

    def explore(self):
        modSort = self.model.modules.keys()
        modSort.sort()
        return modSort

    def refreshCtrl(self):
        ListCtrlView.refreshCtrl(self)
        i = 0
        modSort = self.model.modules.keys()
        modSort.sort()
        for mod in modSort:
            # XXX Show a broken icon as default
            imgIdx = -1
            modTpe = 'Unknown'
            if self.model.moduleModels.has_key(mod):
                imgIdx = self.model.moduleModels[mod].imgIdx
                modTpe = self.model.moduleModels[mod].modelIdentifier
            else:
                self.model.idModel(mod)
                if self.model.moduleModels.has_key(mod):
                    imgIdx = self.model.moduleModels[mod].imgIdx
                    modTpe = self.model.moduleModels[mod].modelIdentifier

            appMod = self.model.modules[mod]

            if appMod[0]:
                modTpe = '*%s*'%modTpe

            i = self.addReportItems(i, (mod, modTpe, appMod[1], appMod[2]), imgIdx)

        self.pastelise()

    def OnOpen(self, event):
        if self.selected >= 0:
            # XXX maybe this should be done in the browsing framework
            self.model.openModule(self.GetItemText(self.selected))
            self.model.prevSwitch = self


    def OnAdd(self, event):
        self.model.viewAddModule()

    def OnEdit(self, event):
        name = self.GetItemText(self.selected)
        dlg = wxTextEntryDialog(self, 'Set the description of the module',
            'Edit item', self.model.modules[name][1])
        try:
            if dlg.ShowModal() == wxID_OK:
                answer = dlg.GetValue()
                self.model.editModule(name, name, self.model.modules[name][0],
                      answer)
                self.model.update()
                self.model.notify()
        finally:
            dlg.Destroy()

    def OnRemove(self, event):
        if self.selected >= 0:
            if not self.model.modules[self.GetItemText(self.selected)][0]:
                self.model.removeModule(self.GetItemText(self.selected))
            else:
                wxMessageBox('Cannot remove the main frame of an application',
                    'Module remove error')

    def OnImports(self, events):
        wxBeginBusyCursor()
        try:
            self.model.showImportsView()
        finally:
            wxEndBusyCursor()

        if self.model.views.has_key('Imports'):
            self.model.views['Imports'].focus()
        self.model.update()
        self.model.notify()

    def OnOpenAll(self, event):
        modules = self.model.modules.keys()
        modules.sort()
        for mod in modules:
            try:
                self.model.editor.openOrGotoModule(\
                  self.model.modules[mod][2])
            except: pass

    def addFindResults(self, pattern, mapResults):
        """ mapResult is map of tuples where
            Key - 'Module', file name
            Value - ('Line no', 'Col', 'Text')
        """
        from FindResults import FindResults
        name = 'Results: ' + pattern
        if not self.model.views.has_key(name):
            resultView = self.model.editor.addNewView(name, FindResults)
        else:
            resultView = self.model.views[name]
        resultView.tabName = name
        resultView.results = mapResults
        resultView.findPattern = pattern
        resultView.refresh()
        resultView.focus()

    def OnFind(self, event):
        import FindReplaceDlg
        FindReplaceDlg.find(self, self.model.editor.finder, self)

    def OnMakeMain(self, event):
        if self.selected >= 0:
            self.model.changeMainFrameModule(self.GetItemText(self.selected))


class AppModuleDocView(ModuleDocView):
    viewName = 'Application Documentation'

    def OnLinkClicked(self, linkinfo):
        url = linkinfo.GetHref()

        if url[0] == '#':
            self.base_OnLinkClicked(linkinfo)
        else:
            mod = path.splitext(url)[0]
            newMod, cntrl = self.model.openModule(mod)
            view  = newMod.editor.addNewView(ModuleDocView.viewName, ModuleDocView)
            view.refreshCtrl()
            view.focus()

    def genModuleListSect(self):
        modLst = []
        modNames = self.model.modules.keys()
        modNames.sort()
        for amod in modNames:
            desc = self.model.modules[amod][1].strip()
            modLst.append('<tr><td width="25%%"><a href="%s.html">%s</a></td><td>%s</td></tr>' %(amod, amod, desc))

        return '<table BORDER=0 CELLSPACING=0 CELLPADDING=0>'+'<BR>'.join(modLst)+'</table>', modNames

    def genModuleSect(self, page):
        classList, classNames = self.genClassListSect()
        funcList, funcNames = self.genFuncListSect()
        module = self.model.getModule()
        modBody = wxwAppModuleTemplate % { \
          'ModuleSynopsis': module.getModuleDoc(),
          'Module': self.model.moduleName,
          'ModuleList': self.genModuleListSect()[0],
          'ClassList': classList,
          'FunctionList': funcList,
       }

        return self.genFunctionsSect(\
            self.genClassesSect(page + modBody, classNames), funcNames)

#        return self.genClassesSect(page + modBody, classNames)

class AppCompareView(ListCtrlView, CloseableViewMix):
    gotoLineBmp = 'Images/Editor/GotoLine.png'

    viewName = 'App. Compare'
    def __init__(self, parent, model):
        CloseableViewMix.__init__(self, 'compare results')
        ListCtrlView.__init__(self, parent, model, wxLC_REPORT,
          ( ('Do diff', self.OnGoto, self.gotoLineBmp, ''), ) +\
           self.closingActionItems, 0)

        self.InsertColumn(0, 'Module', width = 100)
        self.InsertColumn(1, 'Differs from', width = 450)
        self.InsertColumn(2, 'Result', width = 75)

        self.results = {}
        self.listResultIdxs = []
        self.tabName = 'App. Compare'
        self.active = true
        self.model = model
        self.compareTo = ''

    def refreshCtrl(self):
        ListCtrlView.refreshCtrl(self)

        from Models.PythonEditorModels import BaseAppModel
        otherApp = BaseAppModel('', self.compareTo, '', self.model.editor, true, {})

        from Explorers.Explorer import openEx
        otherApp.transport = openEx(self.compareTo)

        otherApp.load()
        otherApp.readModules()

        filename, otherFilename = self.model.assertLocalFile(), otherApp.assertLocalFile()

        i = 0
        # Compare apps
        if not cmp(filename, otherFilename):
            i = self.addReportItems(i,
                  (path.splitext(path.basename(filename))[0], otherFilename,
                   'changed'))

        # Find changed modules and modules not occuring in other module
        for module in self.model.modules.keys():
            if otherApp.modules.has_key(module):
                otherFile = otherApp.assertLocalFile(otherApp.moduleFilename(module))
                filename = self.model.assertLocalFile(self.model.moduleFilename(module))
                try:
                    if not cmp(filename, otherFile):
                        i = self.addReportItems(i, (module, otherFile, 'changed') )
                except OSError:
                    pass
            else:
                i = self.addReportItems(i, (module, '', 'deleted') )

        # Find modules only occuring in other module
        for module in otherApp.modules.keys():
            if not self.model.modules.has_key(module):
                #otherFile = otherApp.moduleFilename(module)
                i = self.addReportItems(i, (module, '', 'added') )

        self.pastelise()

    def OnGoto(self, event):
        if self.selected >= 0:
            module = self.GetItemText(self.selected)
            model, controller = self.model.openModule(module)
            otherModule = self.GetItem(self.selected, 1).GetText()
            if otherModule:
                controller.OnDiffModules(filename=otherModule)

class TextInfoFileView(SourceViews.EditorStyledTextCtrl):
    viewName = 'TextInfo'
    def __init__(self, parent, model):
        SourceViews.EditorStyledTextCtrl.__init__(self, parent, -1,
          model, (), 0)
        self.active = true
        SourceViews.EVT_STC_UPDATEUI(self, self.GetId(), self.OnUpdateUI)
        self.model.loadTextInfo(self.viewName)

    def OnUpdateUI(self, event):
        # don't update if not fully initialised
        if hasattr(self, 'pageIdx'):
            self.updateViewState()

    def getModelData(self):
        return self.model.textInfos[self.viewName]

    def setModelData(self, data):
        self.model.textInfos[self.viewName] = data
        if self.viewName not in self.model.unsavedTextInfos:
            self.model.unsavedTextInfos.append(self.viewName)

class AppREADME_TIFView(TextInfoFileView):
    viewName = 'Readme.txt'

class AppTODO_TIFView(TextInfoFileView):
    viewName = 'Todo.txt'

class AppBUGS_TIFView(TextInfoFileView):
    viewName = 'Bugs.txt'

class AppCHANGES_TIFView(TextInfoFileView):
    viewName = 'Changes.txt'
