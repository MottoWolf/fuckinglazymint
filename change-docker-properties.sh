sed -i '/OPTIONS=.*/c\OPTIONS="--selinux-enabled --log-driver=journald --insecure-registry 172.30.0.0/16"' /etc/sysconfig/docker
