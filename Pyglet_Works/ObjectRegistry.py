from pgedraw import basic as Prims #Primatives
import pyglet
import logging
import Config
from Structures import Pod

class ObjectRegistry(object):

	def __init__(self, Interface):
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger('ObjectRegistry')
            self.logger.debug('ObjectRegistry')
            self.logger.debug('__init__')

            ## Get Config
            self.config = Config.Config()

            ## POD REGISTRY
            self.pod_registry = []

            ## Object Dictionary
            self.objects = dict()
            self.objects['case_1'] = dict()

            ## Pods
            self.objects['case_1']['pod_1'] = self.createPod(self.config.X_ZERO, 0 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP)
            self.objects['case_1']['pod_2'] = self.createPod(self.config.X_ZERO, 1 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP)
            self.objects['case_1']['pod_3'] = self.createPod(self.config.X_ZERO, 2 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH, self.config.CASE_1_F_GROUP)
            #self.objects['case_1']['pod_4'] = self.createPod(self.X_ZERO, 3 * self.config.CASE_1_POD_SPACING, Interface.CASE_1_BATCH, self.CASE_1_F_GROUP)

            self.linkPods()

            ## Track
            self.objects['case_1']['track'] = self.createTrack(self.config.X_ZERO, self.config.Y_ZERO, self.config.CASE_1_BATCH, self.config.CASE_1_B_GROUP)


	def createPod(self, x, y, case_batch, case_group):
            ## Create Pod
            sprite = pyglet.sprite.Sprite(self.config.POD_IMAGE, x, y, batch=case_batch, group=case_group)
            sprite.scale = .2

            ## Attach to registry
            list_index = len(self.pod_registry)
            pod = Pod(sprite, pod_ahead=None, pod_behind=None, default_velocity=self.config.POD_VEL, ID=list_index)
            self.pod_registry.append(pod)

            self.logger.debug('----pod created----')
            self.logger.debug('pod x: {} | pod y: {}'.format(pod.SPRITE.x, pod.SPRITE.y))

        def linkPods(self):
            ## Link pods
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

            self.logger.debug('----track created----')
            self.logger.debug('track x: {} | track y: {}'.format(track.x, track.y))
            return track
