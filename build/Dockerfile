FROM python:3.7.3

MAINTAINER zijiehu "1093572262@qq.com"

RUN mkdir -p /app /app/log /app/media
WORKDIR /app
ADD . /app

RUN pip install --no-cache-dir -r build/requirements.txt

EXPOSE 80
CMD ["-n"]