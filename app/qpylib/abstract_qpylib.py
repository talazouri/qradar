from abc import ABCMeta, abstractmethod
import os
import requests
import logging
from flask import url_for
import datetime

loggerName = 'com.ibm.applicationLogger'
logger = 0


class AbstractQpylib(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_app_id(self):
        pass

    def RESTget(self, URL, headers, data=None,
                params=None, json_inst=None, auth=None):
        self.log("REST get issued to " + URL + " " + str(params), "debug")
        return requests.get(URL, params=params,
                            headers=headers, verify=False, auth=auth,
                            data=data, json=json_inst)

    def RESTput(self, URL, headers, data=None,
                params=None, json_inst=None, auth=None):
        self.log("REST put issued to " + URL + " " + str(params), "debug")
        return requests.put(URL, params=params,
                            headers=headers, verify=False, auth=auth,
                            data=data, json=json_inst)

    def RESTpost(self, URL, headers, data=None,
                 params=None, json_inst=None, auth=None):
        self.log("REST post issued to " + URL + " " + str(params), "debug")
        return requests.post(URL, params=params,
                            headers=headers, verify=False, auth=auth,
                            data=data, json=json_inst)

    def RESTdelete(self, URL, headers, data=None,
                   params=None, json_inst=None, auth=None):
        self.log("REST delete issued to " + URL + " " + str(params), "debug")
        return requests.delete(URL, params=params,
                            headers=headers, verify=False, auth=auth,
                            data=data, json=json_inst)

    def RESTunsupported(self, URL, headers, data=None,
                        params=None, json_inst=None, auth=None):
        self.log("REST unsupported issued to " + URL + " " + str(params) +
                 str(headers) + str(data) + str(json_inst) + str(auth), "debug")
        raise ValueError('The REST type passed is not supported')

    def chooseREST(self, RESTtype):
        RESTtype = RESTtype.upper()
        return {
            'GET': self.RESTget,
            'PUT': self.RESTput,
            'POST': self.RESTpost,
            'DELETE': self.RESTdelete,
        }.get(RESTtype, self.RESTunsupported)

    @abstractmethod
    def REST(self, RESTtype, requestURL, headers=None, data=None,
             params=None, json_inst=None, version=None):
        pass

    def choose_log_level(self, level='INFO'):
        if logger == 0:
            return self.logging_not_setup

        level = level.upper()
        return {
            'INFO': logger.info,
            'DEBUG': logger.debug,
            'ERROR': logger.error,
            'WARNING': logger.warning,
            'CRITICAL': logger.critical,
            'EXCEPTION': logger.exception,
        }.get(level, logger.info)

    def logging_not_setup(self, message):
        raise SystemError('You can not call log before logging has been initialised')

    def map_log_level(self, log_level='INFO'):
        log_level = log_level.upper()
        return {
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'CRITICAL': logging.CRITICAL,
        }.get(log_level, logging.INFO)

    @abstractmethod
    def add_log_handler(self, loc_logger):
        pass

    def create_log(self):
        global logger
        global loggerName
        logger = logging.getLogger(loggerName)
        self.add_log_handler(logger)
        self.log("Created log " + loggerName, 'info')

    def set_log_level(self, log_level='INFO'):
        logger.setLevel(self.map_log_level(log_level))

    @abstractmethod
    def get_console_address(self):
        pass

    @abstractmethod
    def root_path(self):
        pass

    def get_root_path(self,relative_path):
        return os.path.join(self.root_path(), relative_path)

    def store_path(self):
        return os.path.join(self.root_path(), 'store')

    def get_store_path(self, relative_path):
        return os.path.join(self.store_path(), relative_path)

    def to_json_dict(self, python_obj, classkey=None):
        """
        Helper function to convert a Python object into a dict
        usable with the JSON REST.
        Recursively converts fields which are also Python objects.
        @param python_obj: Python object to be converted into a dict
        @return dict object containing key:value pairs for the python
        objects fields. Useable with JSON REST.
        """
        if isinstance(python_obj, dict):
            data = {}
            for (k, v) in python_obj.items():
                data[k] = self.to_json_dict(v, classkey)
            return data
        elif hasattr(python_obj, "_ast"):
            return self.to_json_dict(python_obj._ast())
        elif hasattr(python_obj, "__iter__"):
            return [self.to_json_dict(v, classkey) for v in python_obj]
        elif hasattr(python_obj, "__dict__"):
            data = dict([(key, self.to_json_dict(value, classkey))
                         for key, value in python_obj.__dict__.iteritems()
                         if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(python_obj, "__class__"):
                data[classkey] = python_obj.__class__.__name__
            return data
        else:
            return python_obj

    @abstractmethod
    def get_app_base_url(self):
        pass

    def q_url_for(self, endpoint, **values):
        """
        Create an method to wrap the standard Flask url_for())method,
        to include the proxied url through Qradar as a prefix to the
        short-name Flask route name
        """
        url = self.get_app_base_url() + url_for(endpoint, **values)
        self.log("q_url_for==>" + url, 'debug')
        return url

    def map_notification_code(self, log_level='INFO'):
        log_level = log_level.upper()
        return {
            'INFO': "0000006000",
            'DEBUG': "0000006000",
            'ERROR': "0000003000",
            'WARNING': "0000004000",
            'CRITICAL': "0000003000",
        }.get(log_level, "0000006000")

    def log(self, message,  level='info'):
        log_fn = self.choose_log_level(level)
        log_fn(datetime.datetime.now().strftime("%b %d %H:%M:%S ") +
               " 127.0.0.1 " +
               "[APP_ID/" +  self.get_app_id() + "]" +
               "[NOT:" +  self.map_notification_code(level) + "]" +
               "[" + level.upper() + "] " +
               message)

