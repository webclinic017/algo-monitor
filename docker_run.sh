docker image rm algo-monitor
docker build -t algo-monitor .
docker run -it -p 80:80 algo-monitor

