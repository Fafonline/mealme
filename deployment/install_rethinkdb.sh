source ../.env
sudo cat << EOF > /etc/yum.repos.d/rethinkdb.repo
[rethinkdb]
name=RethinkDB
enabled=1
baseurl=https://download.rethinkdb.com/repository/centos/7/x86_64/
gpgkey=https://download.rethinkdb.com/repository/raw/pubkey.gpg
gpgcheck=1
EOF

sudo yum install rethinkdb
rethinkdb --bind all --bind-http ${HOST} --initial-password ${DB_PASSWORD}
#sudo pkill -f rethinkdb