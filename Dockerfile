FROM ubuntu:16.04
COPY src /opt/9spokes/backup
COPY aws /root/.aws
WORKDIR /opt/9spokes/backup
RUN [ "apt-get", "update" ]
RUN [ "apt-get", "install", "awscli", "python2.7", "mariadb-client", "mongodb-clients", "-y" ]
RUN [ "ln", "-s", "/bin/python2.7", "/bin/python" ]
ENTRYPOINT [ "python", "main.py" ]
