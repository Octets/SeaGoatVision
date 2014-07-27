#! /usr/bin/env python

# Copyright (C) 2012-2014  Octets - octets.etsmtl.ca
#
# This file is part of SeaGoatVision.
#
# SeaGoatVision is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Description :
"""

from SeaGoatVision.server.tcp_server import Server
from configuration import Configuration
from resource import Resource
from SeaGoatVision.commons import log
from SeaGoatVision.commons import keys
from SeaGoatVision.server.media.recording.video_recorder import VideoRecorder
from SeaGoatVision.server.media.implementation.movie import Movie
import time
import inspect
import thread
import threading
import os
#from recording.video_recorder import VideoRecorder
from subprocess import Popen, PIPE

logger = log.get_logger(__name__)

KEY_MEDIA = "media"
KEY_FILTERCHAIN = "filterchain"


class CmdHandler:
    def __init__(self):
        """
            Structure of dct_execution
            {"execution_name" : {KEY_FILTERCHAIN : ref, KEY_MEDIA : ref}}
        """
        self.dct_exec = {}
        self.config = Configuration()
        self.resource = Resource()
        # all record history, contains:
        # {"time": ..., "media_name": ..., "path": ...}
        self.lst_record_historic = []
        self._is_keep_alive_media = self.config.get_is_keep_alive_media()
        self.old_rec_dir_path = self.config.get_path_save_record()

        # tcp server for output observer
        self.nb_observer_client = 0
        self.server_observer = Server()
        self.server_observer.start("", 5030)
        self.notify_event_client = {}
        self.id_client_notify = 0

        self.publisher = self.resource.get_publisher()

        # launch command on start
        thread.start_new_thread(self.config.get_dct_cmd_on_start(), (self,))

    def get_publisher(self):
        return self.publisher

    def close(self):
        logger.info("Close cmdHandler and close server.")
        for execution in self.dct_exec.values():
            execution[KEY_MEDIA].close()
        self.server_observer.stop()
        self.publisher.stop()
        self.publisher.deregister(keys.get_key_execution_list())
        self.publisher.deregister(keys.get_key_filter_param())
        self.publisher.deregister(keys.get_key_media_param())
        self.publisher.deregister(keys.get_key_lst_rec_historic())

    @staticmethod
    def _post_command_(arg):
        funct_name = inspect.currentframe().f_back.f_code.co_name
        del arg["self"]
        # special case, observer is reference
        if "observer" in arg:
            arg["observer"] = "REF"
        if arg:
            logger.info("Request : %s - %s" % (funct_name, arg))
        else:
            logger.info("Request : %s" % funct_name)

    #
    # CLIENT ##################################
    #
    def is_connected(self):
        self._post_command_(locals())
        return True

    #
    # EXECUTION FILTER ################################
    #
    def start_filterchain_execution(
            self, execution_name, media_name, filterchain_name, file_name,
            is_client_manager):
        self._post_command_(locals())
        execution = self.dct_exec.get(execution_name, None)

        if execution:
            log.print_function(
                logger.error, "The execution %s is already created." %
                execution_name)
            return False

        filterchain = self.resource.get_filterchain(
            filterchain_name,
            force_new_filterchain=True)
        if not filterchain:
            log.print_function(
                logger.error, "Filterchain %s not exist or contain error." %
                filterchain_name)
            return False

        # Exception, if not media_name, we take the default media_name from the
        # filterchain
        if not media_name:
            media_name = filterchain.get_default_media_name()

        media = self.resource.get_media(media_name)
        if not media:
            log.print_function(
                logger.error,
                "Media %s not exist or you didn't set the default media on \
                filterchain." % media_name)
            return False

        if media.is_media_video() and file_name:
            media.set_file(file_name)

        media.set_is_client_manager(is_client_manager)

        filterchain.set_media_param(media.get_params())
        filterchain.set_execution_name(execution_name)

        media.add_observer(filterchain.execute)
        if self._is_keep_alive_media:
            media.add_observer(self._keep_alive_media)

        self.dct_exec[execution_name] = {
            KEY_FILTERCHAIN: filterchain, KEY_MEDIA: media}

        publisher = self.publisher
        publisher.publish(
            keys.get_key_execution_list(), "+%s" % execution_name)

        for o_filter in filterchain.get_filter():
            o_filter.set_publisher(publisher)
        return True

    def stop_filterchain_execution(self, execution_name):
        self._post_command_(locals())
        execution = self.dct_exec.get(execution_name, None)

        if not execution:
            log.print_function(
                logger.warning,
                "The execution %s is already stopped." % execution_name)
            return False

        # Remove execution image observer from media
        observer = execution.get(KEY_MEDIA, None)
        if observer is None:
            logger.critical(
                "Not found the observer about execution %s" % execution_name)
            return False
        filterchain = execution.get(KEY_FILTERCHAIN, None)
        if filterchain is None:
            logger.critical("Not found the filterchain about \
                execution %s" % execution_name)
            return False

        observer.remove_observer(filterchain.execute)

        # deregiste key
        # TODO move this in filter destroy
        for filter_name in filterchain.get_filter_name():
            key = keys.create_unique_exec_filter_name(execution_name,
                                                      filter_name)
            self.publisher.deregister(key)

        filterchain.destroy()
        del self.dct_exec[execution_name]
        # publish removing filterchain
        self.publisher.publish(
            keys.get_key_execution_list(), "-%s" %
            execution_name)

        return True

    def get_execution_list(self):
        self._post_command_(locals())
        return self.dct_exec.keys()

    def get_execution_info(self, execution_name):
        self._post_command_(locals())
        exec_info = self.dct_exec.get(execution_name, None)
        if not exec_info:
            log.print_function(
                logger.error,
                "Cannot get execution info, it's empty.")
            return
        return {KEY_MEDIA: exec_info[KEY_MEDIA].get_name(),
                KEY_FILTERCHAIN: exec_info[KEY_FILTERCHAIN].get_name()}

    def get_fps_execution(self, execution_name):
        # self._post_command_(locals())
        media = self._get_media(execution_name=execution_name)
        if not media:
            return -1
        return media.get_real_fps()

    #
    # MEDIA ###################################
    #
    def get_media_list(self):
        self._post_command_(locals())
        return {name: self.resource.get_media(name).get_type_media()
                for name in self.resource.get_media_name_list()}

    def cmd_to_media(self, media_name, cmd, value):
        # don't print when it's command frame_media, because it's spam
        if cmd != keys.get_key_media_frame():
            self._post_command_(locals())
        media = self._get_media(media_name=media_name)
        if not media:
            return False
        if media.is_media_streaming():
            log.print_function(
                logger.error,
                "Cannot send a command to a streaming media %s." %
                media_name)
            return False
        return media.do_cmd(cmd, value)

    def get_info_media(self, media_name):
        self._post_command_(locals())
        media = self._get_media(media_name=media_name)
        if not media:
            return {}
        return media.get_info()

    def start_record(self, media_name, path, options):
        self._post_command_(locals())
        """
        options can be like this
            {"compress": 0, "format": "avi"}
        """
        media = self._get_media(media_name=media_name)

        #print "media: " + media.__class__.__name__

        if not media:
            return False
        if media.is_media_video():
            log.print_function(
                logger.error,
                "Cannot start record to a media media %s." % media_name)
            return False
        if self._is_keep_alive_media:
            media.add_observer(self._keep_alive_media)
        return media.start_record(path=path, options=options)

    def stop_record(self, media_name):
        self._post_command_(locals())
        media = self._get_media(media_name=media_name)
        if not media:
            return False
        if media.is_media_video():
            log.print_function(
                logger.error,
                "Cannot stop record to a media media %s." %
                media_name)
            return False
        status = media.stop_record()
        if status:
            # {"time": ..., "media_name": ..., "path": ...}
            record_status = {
                "time": time.time(),
                "media_name": media_name,
                "path": media.get_path_record(),
            }
            self.lst_record_historic.append(record_status)
            self.publisher.publish(keys.get_key_lst_rec_historic(),
                                   record_status)
        else:
            log.print_function(logger.error,
                               "Error to stop the record %s." % media_name)
        return status

    def get_lst_old_record_historic(self):
        self._post_command_(locals())
        root_dir = self.old_rec_dir_path
        if not root_dir:
            root_dir = "."
        lst_old_record_historic = []
        for dirName, subdirList, fileList in os.walk(root_dir, topdown=False):
            for fname in fileList:
                file_ext = os.path.splitext(fname)[1]
                if file_ext == '.avi':
                    file_creation_time = os.path.getctime(dirName + "/" + fname)
                    record_status = {
                        "time": file_creation_time,
                        "name": fname,
                        "path": dirName,
                    }
                    lst_old_record_historic.append(record_status)
        return lst_old_record_historic

    def get_lst_record_historic(self):
        self._post_command_(locals())
        return self.lst_record_historic

    def get_params_media(self, media_name):
        self._post_command_(locals())
        return self._get_param_media(media_name)

    def get_param_media(self, media_name, param_name):
        self._post_command_(locals())
        return self._get_param_media(media_name, param_name)

    def update_param_media(self, media_name, param_name, value):
        # self._post_command_(locals())
        # param_name can be a list or string
        param = self._get_param_media(media_name, param_name)
        if not param:
            return False

        param.set(value)
        return True

    def reset_param_media(self, media_name, param_name):
        self._post_command_(locals())
        # param_name can be a list or string
        lst_param = self._get_lst_param_media(media_name, param_name)

        if not lst_param:
            return False

        for param in lst_param:
            param.reset()
        return True

    def set_as_default_param_media(self, media_name, param_name):
        self._post_command_(locals())
        # param_name can be a list or string
        lst_param = self._get_lst_param_media(media_name, param_name)

        if not lst_param:
            return False

        for param in lst_param:
            param.set_as_default()
        return True

    def save_params_media(self, media_name):
        self._post_command_(locals())
        media = self._get_media(media_name=media_name)
        if not media:
            return False
        return self.config.write_media(media)

    def cut_video(self, video_name, begin, end, cut_video_name):
        self._post_command_(locals())
        video_media = Movie(video_name)
        if not video_media:
            return False
        rec_thread = ThreadRecordCutVideo(video_media, begin, end, cut_video_name, self)
        rec_thread.start()
        return True

    #
    # OBSERVER  #################################
    #
    def add_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name to select the filter
        """
        self._post_command_(locals())
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        return filterchain.add_image_observer(observer, filter_name)

    def set_image_observer(
            self, observer, execution_name, filter_name_old, filter_name_new,
            new_observer=None):
        """
            Inform the server what filter we want to change observer
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name_old , filter to replace
                - string, filter_name_new , filter to use
        """
        if new_observer is None:
            new_observer = observer
        self._post_command_(locals())
        if filter_name_old == filter_name_new:
            log.print_function(
                logger.error,
                "New and old filter_name is equal: %s" %
                filter_name_old)
            return False
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        filterchain.remove_image_observer(observer, filter_name_old)
        return filterchain.add_image_observer(new_observer, filter_name_new)

    def remove_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to remove observer
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name , filter to remove
        """
        self._post_command_(locals())
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        return filterchain.remove_image_observer(observer, filter_name)

    def add_output_observer(self, execution_name):
        """
            attach the output information of execution to tcp_server
            supported only one observer. Add observer to tcp_server
        """
        self._post_command_(locals())
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False

        status = True
        lst_obs = filterchain.get_filter_output_observers()
        if self.server_observer.send not in lst_obs:
            status = filterchain.add_filter_output_observer(
                self.server_observer.send)
        self.nb_observer_client += 1
        return status

    def remove_output_observer(self, execution_name):
        """
            remove the output information of execution to tcp_server
            supported only one observer. remove observer to tcp_server
        """
        self._post_command_(locals())
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        if not filterchain.get_filter_output_observers():
            return True
        self.nb_observer_client -= 1
        if self.nb_observer_client <= 0:
            # protection if go under zero
            if self.nb_observer_client < 0:
                self.nb_observer_client = 0
            return filterchain.remove_filter_output_observer(
                self.server_observer.send)
        return True

    #
    # PUBLISHER  ##################################
    #
    def subscribe(self, key):
        return self.publisher.subscribe(key)

    #
    # CONFIGURATION  ################################
    #

    #
    # FILTERCHAIN  ################################
    #
    def reload_filter(self, filter_name):
        self._post_command_(locals())
        o_filter = self.resource.reload_filter(filter_name)
        if o_filter is None:
            return False
        for execution in self.dct_exec.values():
            filterchain = execution.get(KEY_FILTERCHAIN, None)
            if filterchain:
                filterchain.reload_filter(o_filter)
        return True

    def get_params_filterchain(self, execution_name, filter_name):
        # get actual filter from execution
        # TODO search information from configuration if execution not exist
        self._post_command_(locals())
        return self._get_param_filter(execution_name, filter_name)

    def get_param_filterchain(self, execution_name, filter_name, param_name):
        # get actual filter from execution
        # TODO search information from configuration if execution not exist
        self._post_command_(locals())
        return self._get_param_filter(execution_name, filter_name, param_name)

    def get_filterchain_info(self, filterchain_name):
        self._post_command_(locals())
        return self.resource.get_filterchain_info(filterchain_name)

    def update_param(self, execution_name, filter_name, param_name, value):
        # self._post_command_(locals())
        param = self._get_param_filter(execution_name, filter_name, param_name)
        if not param:
            return False

        param.set(value)
        # TODO update when filter is not running
        o_filter = self._get_filter(execution_name, filter_name)
        o_filter.configure()
        return True

    def reset_param(self, execution_name, filter_name, param_name):
        self._post_command_(locals())
        lst_param = self._get_lst_param_filter(execution_name,
                                               filter_name,
                                               param_name)
        if not lst_param:
            return False

        for param in lst_param:
            param.reset()
        # TODO update when filter is not running
        o_filter = self._get_filter(execution_name, filter_name)
        o_filter.configure()
        return True

    def set_as_default_param(self, execution_name, filter_name, param_name):
        self._post_command_(locals())
        lst_param = self._get_lst_param_filter(execution_name,
                                               filter_name,
                                               param_name)

        if not lst_param:
            return False

        for param in lst_param:
            param.set_as_default()
        # TODO update when filter is not running
        o_filter = self._get_filter(execution_name, filter_name)
        o_filter.configure()
        return True

    def save_params(self, execution_name):
        """Force serialization and overwrite config"""
        self._post_command_(locals())
        filterchain = self._get_filterchain(execution_name)
        if not filterchain:
            return False
        return self.config.write_filterchain(filterchain)

    def get_filterchain_list(self):
        self._post_command_(locals())
        return self.resource.get_filterchain_list()

    def upload_filterchain(self, filterchain_name, s_file_contain):
        self._post_command_(locals())
        return self.resource.upload_filterchain(filterchain_name,
                                                s_file_contain)

    def delete_filterchain(self, filterchain_name):
        self._post_command_(locals())
        return self.resource.delete_filterchain(filterchain_name)

    def modify_filterchain(self, old_filterchain_name,
                           new_filterchain_name, lst_str_filters,
                           default_media):
        self._post_command_(locals())
        return self.resource.modify_filterchain(old_filterchain_name,
                                                new_filterchain_name,
                                                lst_str_filters,
                                                default_media)

    #
    # FILTER  ##################################
    #
    def get_filter_list(self):
        self._post_command_(locals())
        return self.resource.get_filter_info_list()

    #
    # PRIVATE  ##################################
    #
    def _get_execution(self, execution_name):
        dct_execution = self.dct_exec.get(execution_name, {})
        if not dct_execution:
            msg = "Missing execution %s. List execution name: %s" % (
                execution_name, self.dct_exec.keys())
            log.print_function(logger.warning, msg, last_stack=True)
            return
        return dct_execution

    def _get_filterchain(self, execution_name):
        dct_execution = self._get_execution(execution_name)
        if dct_execution is None:
            return
        filterchain = dct_execution.get(KEY_FILTERCHAIN, None)
        if not filterchain:
            msg = "Execution %s hasn't filterchain." % execution_name
            log.print_function(logger.critical, msg, last_stack=True)
            return
        return filterchain

    def _get_media(self, media_name=None, execution_name=None):
        media = None
        if media_name:
            media = self.resource.get_media(media_name)
            if not media:
                log.print_function(
                    logger.error,
                    "Cannot found the media %s." %
                    media_name,
                    last_stack=True)
                return
        elif execution_name:
            dct_execution = self._get_execution(execution_name)
            if not dct_execution:
                return
            media = dct_execution.get(KEY_MEDIA, None)
        return media

    def _get_filter(self, execution_name, filter_name):
        filterchain = self._get_filterchain(execution_name)
        if not filterchain or not filter_name:
            return False
        o_filter = filterchain.get_filter(name=filter_name)
        if not o_filter:
            log.print_function(
                logger.error,
                "Missing filter %s on filterchain %s" % (
                    filter_name, filterchain.get_name()))
            return False
        return o_filter

    def _get_param_filter(self, execution_name, filter_name, param_name=None):
        o_filter = self._get_filter(execution_name, filter_name)
        if not o_filter:
            return
        param = o_filter.get_params(param_name=param_name)
        if not param:
            log.print_function(
                logger.error,
                "Missing param %s on filter %s" % (param_name, filter_name))
        return param

    def _get_lst_param_filter(self, execution_name, filter_name,
                              param_name=None):
        o_filter = self._get_filter(execution_name, filter_name)
        if not o_filter:
            return
        return o_filter.get_lst_params(param_name=param_name)

    def _get_param_media(self, media_name, param_name=None):
        media = self._get_media(media_name=media_name)
        if not media:
            return
        param = media.get_params(param_name=param_name)
        if not param:
            log.print_function(
                logger.error,
                "Missing param %s on media %s" % (param_name, media_name))
        return param

    def _get_lst_param_media(self, media_name, param_name=None):
        media = self._get_media(media_name=media_name)
        if not media:
            return
        return media.get_lst_params(param_name=param_name)

    def _keep_alive_media(self, image):
        pass

    def add_lst_record_historic(self, media_name, path):
        # {"time": ..., "media_name": ..., "path": ...}
        record_status = {
            "time": time.time(),
            "media_name": media_name,
            "path": path,
        }
        self.lst_record_historic.append(record_status)
        self.publisher.publish(keys.get_key_lst_rec_historic(), record_status)


class ThreadRecordCutVideo(threading.Thread):
    """
    """

    def __init__(self, video_media, begin, end, cut_video_name, controller):
        threading.Thread.__init__(self)
        self.video_media = video_media
        self.begin = begin
        self.end = end
        self.cut_video_name = cut_video_name
        self.recorder = VideoRecorder(self._Media())
        self.controller = controller
        #self.resource = Resource()
        #self.publisher = self.resource.get_publisher()

    def run(self):
        #self.video_media.change_frame(self.begin)
        self.recorder.start(123, self.cut_video_name)
        self.video_media.set_position(self.begin)
        for frame_no in range(self.begin, self.end):
            img = self.video_media.next()
            self.recorder.add_image(img)
        self.recorder.stop()
        #mystr[-4:]
        if self.cut_video_name[-4:] == ".avi":
            new_file_name = self.cut_video_name
        else:
            new_file_name = self.cut_video_name + ".avi"
        self.controller.add_lst_record_historic("Movie", new_file_name)

    class _Media():
        def add_observer(self, cp):
            pass

        def remove_observer(self, cb):
            pass
