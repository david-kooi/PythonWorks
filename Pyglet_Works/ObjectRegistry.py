from pgedraw import basic as Prims #Primatives
import pyglet
import logging
import Config
from Structures import Node
from Structures import Pod
from pyglet.text import Label


class ObjectRegistry(object):

	def __init__(self, Interface):
            self.logger = logging.getLogger('ObjectRegistry')
            self.logger.debug('ObjectRegistry')
            self.logger.debug('__init__')


            self.interface = Interface

            ## Get Config
            self.config = Config.Config()

            ## Object Registers
            self.pod_registry = []
            self.node_registry = []
            self.EndNode = None
            self.d_field_registry = []
            self.general_registry = []

            ## Object Dictionary
            self.objects = dict()
            self.objects['case_1'] = dict()

            ## Create Background
            self.createBackground(self.config.GENERAL_BATCH, self.config.GROUP_A)

            ## Track
            self.createTrack(self.config.X_ZERO, self.config.Y_ZERO, self.config.CASE_1_BATCH, self.config.GROUP_A)

            ## Nodes
            start_pos = self.config.CASE_1_NODE_SPACING #+ self.config.CASE_1_NODE_START
            self.createNode(self.config.X_ZERO, 0 * start_pos, self.config.CASE_1_BATCH, self.config.GROUP_B, ID=0)
            self.createNode(self.config.X_ZERO, 1 * start_pos, self.config.CASE_1_BATCH, self.config.GROUP_B, ID=1)
            self.createNode(self.config.X_ZERO, 2 * start_pos, self.config.CASE_1_BATCH, self.config.GROUP_B, ID=2)
            self.createEndNode(self.config.X_ZERO, 3 * start_pos, self.config.CASE_1_BATCH, self.config.GROUP_B) ## 

            ## Node Detection Fields
            self.addDetectionFields()

            ## Pods
            self.createPod(self.config.POD_IMAGE_1, self.config.X_ZERO, 0 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.GROUP_C)
            self.createPod(self.config.POD_IMAGE_2, self.config.X_ZERO, 1 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.GROUP_C)
            #self.createPod(self.config.X_ZERO, 2 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.GROUP_C)
            #self.createPod(self.X_ZERO, 3 * self.config.CASE_1_POD_SPACING, Interface.CASE_1_BATCH, self.GROUP_C)


            ## Labels
            #for pod in self.pod_registry:
             #     self.createLabel(pod=pod, case_batch=self.config.CASE_1_BATCH, case_group=self.config.CASE_1_F_GROUP)

            #self.linkPods()


        def createBackground(self, case_batch, case_group):
            ## Set Background at 0,0 default coordinates
            sprite = pyglet.sprite.Sprite(self.config.BG_IMAGE, 0, 0, batch=case_batch, group=case_group)
            self.general_registry.append(sprite)


        def createLabel(self, pod, case_batch, case_group):
            self.logger.debug("---- Label Created ----")
            self.logger.debug('label x: {} | label y: {}'.format(pod.SPRITE.x, pod.SPRITE.y))
            label = Label(str(pod.ID), x=pod.SPRITE.x, y=pod.SPRITE.y, color=self.config.BLACK, batch=case_batch, group=case_group)

            for pod in self.pod_registry:
                pod.label = label

        def createEndNode(self, x, y, case_batch, case_group):
              sprite = pyglet.sprite.Sprite(self.config.NODE_IMAGE, x, y, batch=case_batch, group=case_group)
              sprite.scale = .5
              self.EndNode = sprite
        def createNode(self, x, y, case_batch, case_group, ID):
              sprite = pyglet.sprite.Sprite(self.config.NODE_IMAGE, x, y, batch=case_batch, group=case_group)
              sprite.scale = .5
  
              node = Node(self.pod_registry, sprite, self.interface.master_clock, ID=ID)
              self.node_registry.append(node)
  
              self.logger.debug('----node created----')
              self.logger.debug('node x: {} | node y: {}'.format(node.SPRITE.x, node.SPRITE.y))
              return node
      
        def addDetectionFields(self):
            ## Create for standard Nodes
            for node in self.node_registry:
                  self.createDetectionField(self.config.X_ZERO, node.SPRITE.y, self.config.CASE_1_BATCH, self.config.GROUP_B)

            ## Create for EndNode
            self.createDetectionField(self.config.X_ZERO, self.EndNode.y, self.config.CASE_1_BATCH, self.config.GROUP_B)

        def createDetectionField(self, x_pos, y_pos, case_batch, case_group):

              sprite = pyglet.sprite.Sprite(self.config.DETECT_IMAGE, x_pos, y_pos, batch=case_batch, group=case_group)
              sprite.visible=False
              self.d_field_registry.append(sprite)

  
        def getNodeByID(self, ID):
              for node in self.node_registry:
                    if node.ID == ID:
                          return node 
  
	def createPod(self, pod_image, x, y, case_batch, case_group):
            ## Create Pod
            sprite = pyglet.sprite.Sprite(pod_image, x, y, batch=case_batch, group=case_group)
            sprite.scale = .5

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
        

