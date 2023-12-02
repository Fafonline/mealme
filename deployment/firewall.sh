yum install firewalld`
systemctl start firewalld
sudo systemctl enable firewalld

firewall-cmd --permanent --add-port=80/tcp
