from util import Util
import logging

class S3():


    def check_bucket(self, bucket):
        return Util.run(["aws", "s3", "ls", "s3://" + bucket])

    @staticmethod
    def stream(bucket, stdin):
        return Util.stream(["aws", "s3", "cp", "-", "s3://" + bucket ], stdin)