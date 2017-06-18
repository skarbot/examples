import sys
from functools import partial

sys.path.append(r'/Users/skar/workspace/venv/pyside_2.7/lib/python2.7/site-packages')

import icon
from PySide import QtGui, QtCore


data = {
    'root': {
        'one': [1, 2, 3, 4, 5],
        'two': [6, 7, 8, 9, 10],
        'three': {
            'third 1': [1, 2, 3, 4, 5],
            'third 2': [6, 7, 8, 9, 10],
            'third 3': {
                'fourth': [11, 12, 13, 14, 15]
            }
        }
    }
}

class Signal(QtCore.QObject):
    done = QtCore.Signal(int)

class worker(QtCore.QRunnable):
    signal = Signal()

    def run(self):
        import time
        time.sleep(10)
        self.signal.done.emit(5)


class TreeItem(object):
    def __init__(self, name, data, parent=None):
        self.name = name
        self.parentItem = parent
        self.itemData = [self.name] + data
        self.childItems = []
        self.instance = 1
        self.thread = worker()
        self.thread.signal.done.connect(self.on_complete)
        QtCore.QThreadPool.globalInstance().start(self.thread)

    def on_complete(self, value):
        self.instance = value

    def __repr__(self):
        return '{} {}'.format(self.name, self.parentItem)

    def addChild(self, item):
        self.childItems = item

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


def get_tree_data(model_data, parent=None):
    return_list = []
    for key, value in model_data.iteritems():
        if type(value) == list:
            return_list.append(
                TreeItem(
                    name=key,
                    data=value,
                    parent=parent))
        else:
            tree_item = TreeItem(
                name=key,
                data=[],
                parent=parent
            )
            value = get_tree_data(value, parent=tree_item)
            tree_item.addChild(value)
            return_list.append(tree_item)
    return return_list


class Model(QtCore.QAbstractItemModel):
    def __init__(self):
        super(Model, self).__init__()
        self.root = get_tree_data(data)[0]
        self.childthreads = []

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.root
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def columnCount(self, parent):
        return 6

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            parentItem = self.root
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            if not childItem in self.childthreads:
                childItem.thread.signal.done.connect(partial(
                    self.updatemode,
                    self.createIndex(row, 0, childItem),
                    self.createIndex(row, 4, childItem)))
                self.childthreads.append(childItem)

            self.childthreads.append(childItem)
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def updatemode(self, inde, rinde, args):
        self.dataChanged.emit(inde, rinde)

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if not parentItem:
            parentItem = self.root

        if parentItem == self.root:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            item = index.internalPointer()
            if index.column() == 1:
                return item.instance

            return item.data(index.column())

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 1:
                return icon.create_icon()


class View(QtGui.QTreeView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent=parent)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    view = View()
    model = Model()
    view.setModel(model)

    view.show()
    sys.exit(app.exec_())
