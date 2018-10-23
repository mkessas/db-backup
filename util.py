from subprocess import Popen, PIPE
import os

class Util():
            
    @staticmethod
    def run(cmd):
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        #rc = p.returncode
        
        return output, err


    @staticmethod
    def stream(cmd):
        p = Popen(" ".join(cmd), stdout=PIPE, shell=True)
        return p.communicate()
