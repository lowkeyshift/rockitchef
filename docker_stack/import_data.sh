# I think this is supposed to fail

cat dump_*.sql | docker exec -i docker_stack_db_1 psql -U rockitmaster recipes
