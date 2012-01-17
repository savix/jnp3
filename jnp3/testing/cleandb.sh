mysql --user=root --password=kartofel hstest -e 'delete from users;'
mysql --user=root --password=kartofel hstest -e 'delete from photos;'
mysql --user=root --password=kartofel hstest -e 'delete from sessions;'

rm -rf /usr/mogdata/dev1/* /usr/mogdata/dev2/*
mysql --user=root --password=kartofel mogilefs -e 'delete from file;'
mysql --user=root --password=kartofel mogilefs -e 'delete from file_on;'

service mogstored restart
