from abc import ABCMeta, abstractmethod
import abc


class Database():

    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def backup_db(self):
        pass
    
    @abc.abstractmethod
    def detect_client(self):
        pass

    @abc.abstractmethod
    def cleanup(self):
        pass
    
    @abc.abstractmethod
    def backup_all_dbs(self):
        pass

    @abc.abstractmethod
    def get_db_names(self):
        pass
