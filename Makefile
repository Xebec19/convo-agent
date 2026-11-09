migrate-up:
	migrate \
	-path migrations/ \
	-database "postgres://postgres:postgres@localhost:5432/myapp?sslmode=disable" \
	-verbose up

migrate-down:
	migrate \
	-path migrations/ \
	-database "postgres://postgres:postgres@localhost:5432/myapp?sslmode=disable" \
	-verbose down

migrate:
	migrate \
	-path migrations/ \
	-database "postgres://postgres:postgres@localhost:5432/myapp?sslmode=disable" \

.PHONY:
	migrate_up migrate_down migrate