#----------------------------------------------------------------------
# Name:        EventCollections.py
# Purpose:     
#
# Author:      Riaan Booysen
#
# Created:     1999
# RCS-ID:      $Id$
# Copyright:   (c) 1999, 2000 Riaan Booysen
# Licence:     GPL
#----------------------------------------------------------------------
# XXX Add another type of event:
# XXX   Old style method overriding
# XXX   These methods would be picked up from the methods of the class in module
# XXX   and not connected to an EVT_*.
# XXX   At first this is only practical with frames as frames are the only
# XXX   design time overrideable control.

# Miscellaneous

##def EVT_ACTIVATE(win, func):
##def EVT_ACTIVATE_APP(win, func):

##def EVT_END_SESSION(win, func):
##def EVT_QUERY_END_SESSION(win, func):
##def EVT_DROP_FILES(win, func):

##def EVT_INIT_DIALOG(win, func):
##def EVT_SYS_COLOUR_CHANGED(win, func):

##def EVT_SHOW(win, func):
##def EVT_MAXIMIZE(win, func):
##def EVT_ICONIZE(win, func):
##def EVT_NAVIGATION_KEY(win, func):
##def EVT_IDLE(win, func):
##def EVT_UPDATE_UI(win, id, func):

### Mouse Events

### EVT_COMMAND
##def EVT_COMMAND(win, id, cmd, func):
##def EVT_COMMAND_RANGE(win, id1, id2, cmd, func):

### Scrolling

### Scrolling, with an id
##def EVT_COMMAND_SCROLL(win, id, func):
##def EVT_COMMAND_SCROLL_TOP(win, id, func):
##def EVT_COMMAND_SCROLL_BOTTOM(win, id, func):
##def EVT_COMMAND_SCROLL_LINEUP(win, id, func):
##def EVT_COMMAND_SCROLL_LINEDOWN(win, id, func):
##def EVT_COMMAND_SCROLL_PAGEUP(win, id, func):
##def EVT_COMMAND_SCROLL_PAGEDOWN(win, id, func):
##def EVT_COMMAND_SCROLL_THUMBTRACK(win, id, func):

###---
##def EVT_SCROLLWIN(win, func):
##def EVT_SCROLLWIN_TOP(win, func):
##def EVT_SCROLLWIN_BOTTOM(win, func):
##def EVT_SCROLLWIN_LINEUP(win, func):
##def EVT_SCROLLWIN_LINEDOWN(win, func):
##def EVT_SCROLLWIN_PAGEUP(win, func):
##def EVT_SCROLLWIN_PAGEDOWN(win, func):
##def EVT_SCROLLWIN_THUMBTRACK(win, func):

### Scrolling, with an id
##def EVT_COMMAND_SCROLLWIN(win, id, func):
##def EVT_COMMAND_SCROLLWIN_TOP(win, id, func):
##def EVT_COMMAND_SCROLLWIN_BOTTOM(win, id, func):
##def EVT_COMMAND_SCROLLWIN_LINEUP(win, id, func):
##def EVT_COMMAND_SCROLLWIN_LINEDOWN(win, id, func):
##def EVT_COMMAND_SCROLLWIN_PAGEUP(win, id, func):
##def EVT_COMMAND_SCROLLWIN_PAGEDOWN(win, id, func):
##def EVT_COMMAND_SCROLLWIN_THUMBTRACK(win, id, func):

### Convenience commands
##def EVT_BUTTON(win, id, func):
##def EVT_CHECKBOX(win, id, func):
##def EVT_CHOICE(win, id, func):
##def EVT_LISTBOX(win, id, func):
##def EVT_LISTBOX_DCLICK(win, id, func):
##def EVT_TEXT(win, id, func):
##def EVT_TEXT_ENTER(win, id, func):
##def EVT_MENU(win, id, func):
##def EVT_MENU_RANGE(win, id1, id2, func):
##def EVT_SLIDER(win, id, func):
##def EVT_RADIOBOX(win, id, func):
##def EVT_RADIOBUTTON(win, id, func):
##def EVT_VLBOX(win, id, func):
##def EVT_COMBOBOX(win, id, func):
##def EVT_TOOL(win, id, func):
##def EVT_TOOL_RCLICKED(win, id, func):
##def EVT_TOOL_ENTER(win, id, func):
##def EVT_CHECKLISTBOX(win, id, func):

### Generic command events

##def EVT_COMMAND_LEFT_CLICK(win, id, func):
##def EVT_COMMAND_LEFT_DCLICK(win, id, func):
##def EVT_COMMAND_RIGHT_CLICK(win, id, func):
##def EVT_COMMAND_RIGHT_DCLICK(win, id, func):
##def EVT_COMMAND_SET_FOCUS(win, id, func):
##def EVT_COMMAND_KILL_FOCUS(win, id, func):
##def EVT_COMMAND_ENTER(win, id, func):

### wxNotebook events
##def EVT_NOTEBOOK_PAGE_CHANGED(win, id, func):
##def EVT_NOTEBOOK_PAGE_CHANGING(win, id, func):

### wxTreeCtrl events

### wxSpinButton

### wxTaskBarIcon
##def EVT_TASKBAR_MOVE(win, func):
##def EVT_TASKBAR_LEFT_DOWN(win, func):
##def EVT_TASKBAR_LEFT_UP(win, func):
##def EVT_TASKBAR_RIGHT_DOWN(win, func):
##def EVT_TASKBAR_RIGHT_UP(win, func):
##def EVT_TASKBAR_LEFT_DCLICK(win, func):
##def EVT_TASKBAR_RIGHT_DCLICK(win, func):

### wxGrid
##def EVT_GRID_SELECT_CELL(win, fn):
##def EVT_GRID_CREATE_CELL(win, fn):
##def EVT_GRID_CHANGE_LABELS(win, fn):
##def EVT_GRID_CHANGE_SEL_LABEL(win, fn):
##def EVT_GRID_CELL_CHANGE(win, fn):
##def EVT_GRID_CELL_LCLICK(win, fn):
##def EVT_GRID_CELL_RCLICK(win, fn):
##def EVT_GRID_LABEL_LCLICK(win, fn):
##def EVT_GRID_LABEL_RCLICK(win, fn):

### wxSashWindow
##def EVT_SASH_DRAGGED(win, id, func):
##def EVT_SASH_DRAGGED_RANGE(win, id1, id2, func):
##def EVT_QUERY_LAYOUT_INFO(win, func):
##def EVT_CALCULATE_LAYOUT(win, func):

### wxListCtrl

###wxSplitterWindow
##def EVT_SPLITTER_SASH_POS_CHANGING(win, id, func):
##def EVT_SPLITTER_SASH_POS_CHANGED(win, id, func):
##def EVT_SPLITTER_UNSPLIT(win, id, func):
##def EVT_SPLITTER_DOUBLECLICKED(win, id, func):


from wxPython.wx import *

class wxMiscEvent :
    pass
""" Collections of event class macros """
EventCategories = {'ActivateEvent': (EVT_ACTIVATE, EVT_ACTIVATE_APP),
'MiscEvent':   (EVT_SIZE,
                EVT_MOVE,
                EVT_CLOSE,
                EVT_PAINT,
                EVT_ERASE_BACKGROUND),

'FocusEvent' : (EVT_SET_FOCUS,
		EVT_KILL_FOCUS),

'KeyEvent' : (  EVT_CHAR, 
                EVT_CHAR_HOOK, 
                EVT_KEY_DOWN, 
                EVT_KEY_UP),

'MouseEvent' : (EVT_LEFT_DOWN, 
                EVT_LEFT_UP, 
                EVT_MIDDLE_DOWN, 
                EVT_MIDDLE_UP,  
                EVT_RIGHT_UP, 
                EVT_MOTION, 
                EVT_LEFT_DCLICK, 
                EVT_MIDDLE_DCLICK, 
                EVT_RIGHT_DCLICK,
                EVT_LEAVE_WINDOW, 
                EVT_ENTER_WINDOW, 
                EVT_MOUSE_EVENTS),

'ScrollEvent' :(EVT_SCROLL,
                EVT_SCROLL_TOP,
                EVT_SCROLL_BOTTOM,
                EVT_SCROLL_LINEUP,
                EVT_SCROLL_LINEDOWN,
                EVT_SCROLL_PAGEUP,
                EVT_SCROLL_PAGEDOWN,
                EVT_SCROLL_THUMBTRACK),

'CmdScrollEvent' : (EVT_COMMAND_SCROLL,
                    EVT_COMMAND_SCROLL_TOP,
                    EVT_COMMAND_SCROLL_BOTTOM,
                    EVT_COMMAND_SCROLL_LINEUP,
                    EVT_COMMAND_SCROLL_LINEDOWN,
                    EVT_COMMAND_SCROLL_PAGEUP,
                    EVT_COMMAND_SCROLL_PAGEDOWN,
                    EVT_COMMAND_SCROLL_THUMBTRACK),

'FrameEvent' : (EVT_ACTIVATE,
                EVT_DROP_FILES,
                EVT_MAXIMIZE,
                EVT_ICONIZE,
                EVT_NAVIGATION_KEY),

'ListEvent' : ( EVT_LIST_BEGIN_DRAG,
                EVT_LIST_BEGIN_RDRAG,
                EVT_LIST_BEGIN_LABEL_EDIT,
                EVT_LIST_END_LABEL_EDIT,
                EVT_LIST_DELETE_ITEM,
                EVT_LIST_DELETE_ALL_ITEMS,
                EVT_LIST_GET_INFO,
                EVT_LIST_SET_INFO,
                EVT_LIST_ITEM_SELECTED,
                EVT_LIST_ITEM_ACTIVATED,
                EVT_LIST_ITEM_DESELECTED,
                EVT_LIST_KEY_DOWN,
                EVT_LIST_INSERT_ITEM,
                EVT_LIST_COL_CLICK,
                EVT_LIST_ITEM_RIGHT_CLICK,
                EVT_LIST_ITEM_MIDDLE_CLICK),

'TreeEvent' : ( EVT_TREE_BEGIN_DRAG,
                EVT_TREE_BEGIN_RDRAG,
                EVT_TREE_BEGIN_LABEL_EDIT,
                EVT_TREE_END_LABEL_EDIT,
                EVT_TREE_GET_INFO,
                EVT_TREE_SET_INFO,
                EVT_TREE_ITEM_EXPANDED,
                EVT_TREE_ITEM_EXPANDING,
                EVT_TREE_ITEM_COLLAPSED,
                EVT_TREE_ITEM_COLLAPSING,
                EVT_TREE_SEL_CHANGED,
                EVT_TREE_SEL_CHANGING,
                EVT_TREE_KEY_DOWN,
                EVT_TREE_DELETE_ITEM),

'AppEvent' : (  EVT_ACTIVATE_APP,
                EVT_END_SESSION,
                EVT_QUERY_END_SESSION,
                EVT_IDLE,
                EVT_UPDATE_UI),

'SpinEvent' : ( EVT_SPIN_UP,
                EVT_SPIN_DOWN,
                EVT_SPIN),

## This was from the docs, it does not seem to be wrapped, assuming
## EVT_COMMAND_SCROLL connects to Spin buttons
##'CmdSpinEvent' : (  EVT_COMMAND_TOP,
##                    EVT_COMMAND_SCROLL,
##                    EVT_COMMAND_TOP,
##                    EVT_COMMAND_BOTTOM,
##                    EVT_COMMAND_LINEUP,
##                    EVT_COMMAND_LINEDOWN,
##                    EVT_COMMAND_PAGEUP,
##                    EVT_COMMAND_PAGEDOWN,
##                    EVT_COMMAND_THUMBTRACK)

}

normalCategories = ['MiscEvent','FocusEvent','KeyEvent','MouseEvent','AppEvent',
'FrameEvent', 'ScrollEvent']
commandCategories = ['ListEvent', 'TreeEvent', 'CmdScrollEvent', 'SpinEvent']