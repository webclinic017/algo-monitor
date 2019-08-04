docker image rm tpessia/pessiaann
docker build -t tpessia/pessiaann .
docker push tpessia/pessiaann
docker image rm tpessia/pessiaann
read -p "Press enter to continue" nothing

