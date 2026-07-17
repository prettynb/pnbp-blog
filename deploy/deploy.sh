# 
# a deployment script for use on Ubuntu 26.04+ server:
# 

apt update && apt upgrade
#reboot

apt-get install -y python3-pip python3-full python3-venv 
apt install fail2ban -y
apt install acl -y 

#useradd -M curtis
#useradd -L curtis # ??? 

mkdir /apps/
#mkdir /apps/logs/
#mkdir /app/logs/blog_api/
#touch /app/logs/blog_api/access.log
#touch /app/logs/blog_api/errors.log

python3 -m venv /apps/venv




echo 'alias activate=". /apps/venv/bin/activate"' >> /root/.bashrc
echo 'activate' >> /root/.bashrc


git clone https://github.com/prettynb/pnbp-blog /apps/blog
# set-up the blog/ .env file ->

chmod -R 777 /apps/
#setfacl -m u:curtis:rwx /apps

#reboot
#which python3
#which pip3

pip3 install wheel gunicorn uvloop httptools uvicorn uvicorn-worker pyjwt
pip3 install -r /apps/blog/requirements.txt

#mkdir ~/ubuntu/notes
#echo 'export NOTE_PATH="~/ubuntu/notes"' >> /root/.bashrc


ufw allow 22
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

sudo iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp --dport 443 -j ACCEPT


apt install nginx

#mkdir /apps/blog/server/
#mkdir /apps/blog/server/units/

rm /etc/nginx/sites-enabled/default

cp pnbp-blog.nginx /etc/nginx/sites-enabled/

update-rc.d nginx enable
service nginx restart


cp pnbp-blog.service /etc/systemd/system/

systemctl enable pnbp-blog
systemctl start pnbp-blog

#python -m pip install --upgrade fastapi starlette tortoise-orm click 
#python -m pip install bcrypt==4.3.0  # (reference as to why 5.0.0+ breaks) 


apt-get install --reinstall ca-certificates
update-ca-certificates

sudo snap install --classic certbot
#sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx -d pnbp-blog.com
#chmod 0755 /etc/letsencrypt/

python deploy.py >> api_user_temp.json

reboot

