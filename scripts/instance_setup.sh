# Instance setup - eg, using medium Ubuntu 64 bit image on aws

sudo apt-get update
sudo apt-get install -y git
git clone http://www.github.com/vsoch/cogat-docker
sudo apt-get install -y apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" >> docker.list
sudo mv docker.list /etc/apt/sources.list.d
sudo apt-get update
sudo apt-get purge lxc-docker
apt-cache policy docker-engine
sudo apt-get update
sudo apt-get install -y docker-engine
sudo service docker start
# sudo docker run hello-world
sudo groupadd docker
sudo usermod -aG docker ubuntu
curl -L https://github.com/docker/compose/releases/download/1.7.1/docker-compose-`uname -s`-`uname -m` > docker-compose
chmod u+x docker-compose
sudo mv docker-compose /usr/local/bin
sudo shutdown -r 1 # reboot
# then docker-compose up -d
# cd cogat-docker
# You will need to create the .env and cognitive/secrets.py files
# docker-compose up -d
# the command above will download the images, and start the application in detached.

# You will need to ssh into the instance to migrate the database, eg:
# docker exec -it [CONTAINER ID] bash
# (get container ids with docker ps)
# To migrate: python scripts/migrate_database.py

