from pgedraw import basic as Prims #Primatives
import pyglet
import logging
import Config
from Structures import Node
from Structures import Pod
from pyglet.text import Label


class ObjectRegistry(object):

	def __init__(self, Interface):
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger('ObjectRegistry')
            self.logger.debug('ObjectRegistry')
            self.logger.debug('__init__')


            self.interface = Interface

            ## Get Config
            self.config = Config.Config()

            ## Object Registers
            self.pod_registry = []
            self.node_registry = []
            self.general_registry = []

            ## Object Dictionary
            self.objects = dict()
            self.objects['case_1'] = dict()

            ## Nodes
            start_pos = self.config.CASE_1_NODE_SPACING #+ self.config.CASE_1_NODE_START
            #self.createNode(self.config.X_ZERO, 0 * start_pos, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP, ID=0)
            self.createNode(self.config.X_ZERO, 0 * start_pos, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP, ID=1)
            #self.createNode(self.config.X_ZERO, 2 * start_pos, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP, ID=2)

            ## Pods
            #self.createPod(self.config.X_ZERO, 0 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP)
            self.createPod(self.config.X_ZERO, 1 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP)
            #self.createPod(self.config.X_ZERO, 2 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP)
            #self.createPod(self.X_ZERO, 3 * self.config.CASE_1_POD_SPACING, Interface.CASE_1_BATCH, self.CASE_1_F_GROUP)


            ## Labels
            #for pod in self.pod_registry:
             #     self.createLabel(pod=pod, case_batch=self.config.CASE_1_BATCH, case_group=self.config.CASE_1_F_GROUP)

            #self.linkPods()


            ## Track
            self.createTrack(self.config.X_ZERO, self.config.Y_ZERO, self.config.CASE_1_BATCH, self.config.CASE_1_B_GROUP)


        def createLabel(self, pod, case_batch, case_group):
            self.logger.debug("---- Label Created ----")
            self.logger.debug('label x: {} | label y: {}'.format(pod.SPRITE.x, pod.SPRITE.y))
            label = Label(str(pod.ID), x=pod.SPRITE.x, y=pod.SPRITE.y, color=self.config.BLACK, batch=case_batch, group=case_group)

            for pod in self.pod_registry:
                pod.label = label

	def createPod(self, x, y, case_batch, case_group):
            ## Create Pod
            sprite = pyglet.sprite.Sprite(self.config.POD_IMAGE, x, y, batch=case_batch, group=case_group)
            sprite.scale = .2

            ## Attach to registry
            list_index = len(self.pod_registry)
            pod = Pod(sprite, default_velocity= self.config.POD_VEL, ID=list_index)
            self.pod_registry.append(pod)

            self.logger.debug('----pod created----')
            self.logger.debug('pod x: {} | pod y: {}'.format(pod.SPRITE.x, pod.SPRITE.y))

        def linkPods(self):
            for idx, pod in enumerate(self.pod_registry):
                  if pod == self.pod_registry[-1]:
                        pod.pod_ahead = self.pod_registry[0]
                        pod.pod_behind = self.pod_registry[-2]
                  else:
                        pod.pod_ahead = self.pod_registry[idx+1]
                        pod.pod_behind = self.pod_registry[idx-1]

                  self.logger.debug('pod: {}'.format(pod.ID))
                  self.logger.debug('pod_ahead: {}'.format(pod.pod_ahead.ID))
                  self.logger.debug('pod_behind: {}'.format(pod.pod_behind.ID))



        def createTrack(self, x, y, case_batch, case_group):
            track = pyglet.sprite.Sprite(self.config.TRACK_IMAGE, x, y, batch=case_batch, group=case_group)
            track.scale = 1

            self.general_registry.append(track)

            self.logger.debug('----track created----')
            self.logger.debug('track x: {} | track y: {}'.format(track.x, track.y))
        def createNode(self, x, y, case_batch, case_group, ID):
            sprite = pyglet.sprite.Sprite(self.config.NODE_IMAGE, x, y, batch=case_batch, group=case_group)
            sprite.scale = .45

            node = Node(self.pod_registry, sprite, self.interface.master_clock, ID=ID)
            self.node_registry.append(node)

            self.logger.debug('----node created----')
            self.logger.debug('node x: {} | node y: {}'.format(node.SPRITE.x, node.SPRITE.y))
            return node

