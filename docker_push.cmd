docker image rm tpessia/algo-monitor
docker build -t tpessia/algo-monitor .
docker push tpessia/algo-monitor
docker image rm tpessia/algo-monitor
pause
