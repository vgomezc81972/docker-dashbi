
#creacion imagen VITOTOJU -- DIANA 4nov
docker build -t dashbi:v1 .

#Ejecucion de la imagen
docker run -p 8050:8050 dashbi:v1


