from util import Util
import logging

class S3():


    def check_bucket(self, bucket):
        Util.stream(["aws", "s3", "ls", "s3://" + bucket])
        date = Util.stream(["date", "+%Y%m%d%H%M%S"])
        stream = Util.stream(["aws", "s3", "cp", "-", "s3://" + bucket + "/last_updated.txt"], date.stdout)
        date.stdout.close()

        return stream.communicate()

    @staticmethod
    def stream(bucket, stdin):
        return Util.stream(["aws", "s3", "cp", "-", "s3://" + bucket ], stdin)