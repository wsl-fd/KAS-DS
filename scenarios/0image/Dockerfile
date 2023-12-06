FROM python:3.8.10-slim-buster
RUN pip3 install requests numpy ajpy redis PyMySQL
# ENTRYPOINT ["python3", "-u", "/home/normal.py"]
# ['', '/usr/local/lib/python38.zip', '/usr/local/lib/python3.8', '/usr/local/lib/python3.8/lib-dynload', '/usr/local/lib/python3.8/site-packages']
COPY BaseExploit.py /usr/local/lib/python3.8/site-packages
CMD []