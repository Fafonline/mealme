#!/bin/bash

check_firewall() {
    if ! command -v firewalld &> /dev/null; then
        echo "Installing firewalld..."
        sudo yum install -y firewalld
        echo "Firewalld installed."
    fi
}

start_firewall() {
    check_firewall
    echo "Starting firewall..."
    sudo systemctl start firewalld
    sudo systemctl enable firewalld
    sudo firewall-cmd --permanent --add-port=80/tcp
    sudo firewall-cmd --permanent --add-port=22/tcp
    sudo firewall-cmd --permanent --add-port=5000/tcp
    sudo firewall-cmd --permanent --add-port=28015/tcp
    sudo firewall-cmd --reload
    echo "Firewall started and rules applied."
}

reset_docker_ip_table() {
    sudo service docker stop 
    sudo iptables -t nat -F 
    sudo service docker start
}

stop_firewall() {
    echo "Stopping firewall..."
    sudo systemctl stop firewalld
    echo "Firewall stopped."
    reset_docker_ip_table
}

# Check for command-line argument
if [ "$1" == "start" ]; then
    start_firewall
elif [ "$1" == "stop" ]; then
    stop_firewall
else
    echo "Usage: $0 {start|stop}"
    exit 1
fi
