from pgedraw import basic as Prims #Primatives
import pyglet
import logging
import Config

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
            self.objects['case_1']['pod_1'] = self.createPod(self.config.X_ZERO, 0 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH)
            self.objects['case_1']['pod_2'] = self.createPod(self.config.X_ZERO, 1 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH)
            self.objects['case_1']['pod_3'] = self.createPod(self.config.X_ZERO, 2 * self.config.CASE_1_POD_SPACING, self.config.CASE_1_BATCH)
            #self.objects['case_1']['pod_4'] = self.createPod(self.X_ZERO, 3 * self.CASE_1_POD_SPACING, Interface.CASE_1_BATCH)

            ## Track
            self.objects['case_1']['track'] = self.createTrack(self.config.X_ZERO, self.config.Y_ZERO, self.config.CASE_1_BATCH)


	def createPod(self, x, y, case_batch):
            ## Create Pod
            pod = pyglet.sprite.Sprite(self.config.POD_IMAGE, x, y, batch=case_batch)
            pod.scale = .2

            ## And attach to registry
            self.pod_registry.append(pod)

            self.logger.debug('----pod created----')
            self.logger.debug('pod x: {} | pod y: {}'.format(pod.x, pod.y))
            return pod
        def createTrack(self, x, y, case_batch):
            track = pyglet.sprite.Sprite(self.config.TRACK_IMAGE, x, y, batch=case_batch)
            track.scale = 1

            self.logger.debug('----track created----')
            self.logger.debug('track x: {} | pod y: {}'.format(track.x, track.y))
            return track
