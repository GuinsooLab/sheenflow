dev_webapp:
	REACT_APP_BACKEND_ORIGIN="http://127.0.0.1:3333" yarn start

generate-graphql:
	yarn workspace @sheenlet/sheenlet-core @sheenlet/generate-graphql

generate-perms:
	yarn workspace @sheenlet/sheenlet-core generate-perms

ts:
	yarn workspace @sheenlet/sheenlet-app ts && yarn workspace @sheenlet/sheenlet-core ts && yarn workspace @sheenlet/ui ts

lint:
	yarn workspace @sheenlet/sheenlet-app lint && yarn workspace @sheenlet/sheenlet-core lint && yarn workspace @sheenlet/ui lint

test:
	yarn workspace @sheenlet/sheenlet-core jest && yarn workspace @sheenlet/ui jest

jest:
	yarn workspace @sheenlet/sheenlet-core jest && yarn workspace @sheenlet/ui jest
