from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import inspect

class MockJsonrpcServer():
    def __init__(self, port):
        pass
        #self.server = SimpleJSONRPCServer(('', port), logRequests=False)

    def register(self):
        # register all rpc callback
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, method in methods:
            if name in ('__init__', 'register'):
                continue
            self.server.register_function(method, name)
            
    def add_image_observer(self, observer, execution_name, filter_name):
        pass

    def add_output_observer(self, execution_name):
        pass

    def cmd_to_media(self, media_name, cmd, value):
        pass

    def cut_video(self, video_name, begin, end, cut_video_name):
        pass

    def delete_filterchain(self, filterchain_name):
        pass

    def get_count_keys(self):
        pass

    def get_execution_info(self, execution_name):
        pass

    def get_execution_list(self):
        pass

    def get_default_media_name(self):
        pass

    def get_filter_list(self):
        pass

    def get_filterchain_info(self, filterchain_name):
        pass

    def get_filterchain_list(self):
        pass

    def get_fps_execution(self, execution_name):
        pass

    def get_info_media(self, media_name):
        pass

    def get_lst_old_record_historic(self):
        pass

    def get_lst_record_historic(self):
        pass

    def get_media_list(self):
        pass

    def get_param_filterchain(self, execution_name, filter_name, param_name):
        pass

    def get_param_media(self, media_name, param_name):
        pass

    def get_params_filterchain(self, execution_name, filter_name, param_name):
        pass

    def get_params_media(self, media_name):
        pass

    def is_connected(self):
        pass

    def modify_filterchain(self,
                           old_filterchain_name,
                           new_filterchain_name,
                           lst_str_filters,
                           default_media):
        pass

    def reload_filter(self, filter_name):
        pass

    def remove_image_observer(self, observer, execution_name, filter_name):
        pass

    def remove_output_observer(self, execution_name):
        pass

    def reset_param(self, execution_name, filter_name, param_name):
        pass

    def reset_param_media(self, media_name, param_name):
        pass

    def save_params(self, execution_name):
        pass

    def save_params_media(self, media_name):
        pass

    def set_as_default_param(self, execution_name, filter_name, param_name):
        pass

    def set_as_default_param_media(self, media_name, param_name):
        pass

    def set_image_observer(self,
                           observer,
                           execution_name,
                           filter_name_old,
                           filter_name_new,
                           new_observer=None):
        pass

    def start_filterchain_execution(self,
                                    execution_name,
                                    media_name,
                                    filterchain_name,
                                    file_name,
                                    is_client_manager):
        pass

    def start_record(self, media_name, path, options):
        pass

    def stop_filterchain_execution(self, execution_name):
        pass

    def stop_record(self, media_name):
        pass

    def subscribe(self, key):
        pass

    def update_param(self, execution_name, filter_name, param_name, value):
        pass

    def update_param_media(self, media_name, param_name, value):
        pass

    def upload_filterchain(self, filterchain_name, s_file_contain):
        pass

    def default_call(self):
        pass
    
if __name__ == '__main__':
    x = MockJsonrpcServer(9000)
    z = inspect.getmembers(x, predicate=inspect.ismethod)
    
