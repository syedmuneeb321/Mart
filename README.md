poetry run uvicorn src.main:app --reload 
poetry run pytest 


docker commands 
stop container: "docker stop conttainer_id/container_name"
remove container: "docker rm conttainer_id/container_name"
check cotnainer remove successfull: docker ps -a
check images : docker images 
remove image : docker rmi image_id/image_name 

run compose yaml file: docker compose up -d
kil command : docker compose down

docker compose command link:[text](https://github.com/panaverse/learn-generative-ai/blob/main/05_microservices_all_in_one_platform/14_docker/04_compose/README.md)
