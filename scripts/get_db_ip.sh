# This should eventually go into some Dockerfile to make sure regardless of the address, it
# can be referred to as graphdb in the script
ip_address=`docker inspect --format="{{.NetworkSettings.IPAddress}}" app_graphdb_1`
echo $ip_address graphdb | sudo tee -a /etc/hosts
