from abc import ABCMeta, abstractmethod
import abc


class Database():

    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def do_backup(self):
        pass
    
    @abc.abstractmethod
    def detect_client(self):
        pass

    @abc.abstractmethod
    def cleanup(self):
        pass
