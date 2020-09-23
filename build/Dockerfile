# build with:
# docker build -t py_wbn .

FROM python:3.8.0-slim

# ENV

# # set TERM so clear works
# ENV TERM=cygwin

# # set display port to avoid crash
# ENV DISPLAY=:99

# # set timezone
# ENV TZ=America/Chicago
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# apt-get

RUN apt-get update && apt-get -y update

# install python libs

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir pandas numpy pathlib
RUN pip install --no-cache-dir datetime
RUN pip install --no-cache-dir wolframalpha

# get script files

COPY python/ /python/
RUN chmod -R 0777 /python
RUN chmod 0744 /python/wbn_email_name.py

# set up output
RUN mkdir -p /python/output

# run script
CMD ["python", "-u", "/python/wbn_email_name.py"]