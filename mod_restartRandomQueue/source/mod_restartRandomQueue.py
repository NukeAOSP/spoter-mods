# -*- coding: utf-8 -*-
import BigWorld
import constants
from PlayerEvents import g_playerEvents
# noinspection PyProtectedMember
from gui.Scaleform.daapi.view.lobby.battle_queue import _QueueProvider
from gui.prb_control import prbEntityProperty
from helpers import dependency
from skeletons.gui.lobby_context import ILobbyContext


class Mod:
    lobbyContext = dependency.descriptor(ILobbyContext)
    def __init__(self):
        g_playerEvents.onQueueInfoReceived += self.processQueueInfo
        self._count = 0
        self._exitCallback = None

    @prbEntityProperty
    def prbEntity(self):
        return None

    def processQueueInfo(self, _):
        if self.prbEntity is None:
            return
        if self.lobbyContext.isFightButtonPressPossible() and self.prbEntity.getQueueType() == constants.ARENA_GUI_TYPE.RANDOM and self._count:
            self.prbEntity.exitFromQueue()
            self.restartEnqueueRandom()
        self._count += 1

    def restartEnqueueRandom(self):
        if not self.prbEntity.isInQueue():
            self.prbEntity.exitFromQueue()
            return
        self._exitCallback = BigWorld.callback(0.1, self.restartEnqueueRandom)

    def start(self):
        self._count = 0
        self._exitCallback = None


mod = Mod()


def newStart(self):
    oldStart(self)
    mod.start()


oldStart = _QueueProvider.start
_QueueProvider.start = newStart

print '[LOAD_MOD]:  [mod_restartRandomQueue 1.05 (16-06-2019), by spoter]'
