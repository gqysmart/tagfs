#
# Copyright 2011 Markus Pielmeier
#
# This file is part of tagfs.
#
# tagfs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tagfs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tagfs.  If not, see <http://www.gnu.org/licenses/>.
#

from tagfs.cache import cache
from tagfs.node import Stat, ItemLinkNode, DirectoryNode
from tagfs.node_untagged_items import UntaggedItemsDirectoryNode
from tagfs.node_filter_context import ContextValueListDirectoryNode

class RootDirectoryNode(DirectoryNode):
    
    def __init__(self, itemAccess):
        self.itemAccess = itemAccess

    @property
    def attr(self):
        s = super(RootDirectoryNode, self).attr

        # TODO why nlink == 2?
        s.st_nlink = 2

        # TODO write test case which tests st_mtime == itemAccess.parseTime
        s.st_mtime = self.itemAccess.parseTime
        s.st_ctime = s.st_mtime
        s.st_atime = s.st_mtime

        return s

    @property
    @cache
    def items(self):
        return self.itemAccess.taggedItems

    @property
    def contexts(self):
        c = set()

        for item in self.items:
            for t in item.tags:
                context = t.context

                if context is None:
                    continue

                c.add(t.context)

        return c

    @property
    def _entries(self):
        yield UntaggedItemsDirectoryNode('.untagged', self.itemAccess)

        for context in self.contexts:
            yield ContextValueListDirectoryNode(self.itemAccess, self, context)

        for item in self.items:
            yield ItemLinkNode(item)
