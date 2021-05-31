FROM python:3

ADD ./patch_tech_test /patch_tech_test/
RUN pip install -U pip
RUN pip install -r /patch_tech_test/requirements.pip
ENTRYPOINT sh /patch_tech_test/docker-entrypoint.sh
