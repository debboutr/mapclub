= steps to dump and rebuild DB =
* Backup..
`docker exec -i django-on-docker-db-1 /usr/local/bin/pg_dump -U mapclub mapclub_dev > postgres-backup.sql`
  
* Restore...
`docker cp postgres-backup.sql django-on-docker-db-1:/tmp`
`docker exec django-on-docker-db-1 psql -U mapclub -d mapclub_dev -f /tmp/postgres-backup.sql`

= backup mediafiles won't need to be done in dev, but in prod =
* `zip -r mfiles.zip app/mediafiles`
* 
