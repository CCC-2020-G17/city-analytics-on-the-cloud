# tag 
docker tag src_restful_api_server mgsweet/server_restful_api_server
docker tag src_nginx mgsweet/server_nginx
# push to docker hub
docker push mgsweet/server_nginx
docker push mgsweet/server_restful_api_server