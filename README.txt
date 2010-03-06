Installation:

apt-get install python-virtualenv
virtualenv .
. bin/activate
apt-get install python-dev
easy_install debshots...
paster make-config debshots my.ini
apt-get install memcached python-memcache
aptitude install daemontools daemontools-run
mkdir /etc/service/debshots
Create a file /etc/service/debshots/run...
chmod +x /etc/service/debshots
svc -u /etc/service/debshots
(logging?)

