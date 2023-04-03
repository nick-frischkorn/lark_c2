FROM itsafeaturemythic/python38_sanic_c2profile:0.0.6

RUN  apt-get update
COPY ["requirements.txt", "/requirements.txt"]
RUN pip install -r /requirements.txt

ENTRYPOINT ["/Mythic/mythic/c2_service.sh"]