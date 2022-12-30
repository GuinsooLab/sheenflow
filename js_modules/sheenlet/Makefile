dev_webapp:
	REACT_APP_BACKEND_ORIGIN="http://127.0.0.1:3333" yarn start

generate-graphql:
	yarn workspace sheenlet-core generate-graphql

generate-perms:
	yarn workspace sheenlet-core generate-perms

ts:
	yarn workspace sheenlet-app ts && yarn workspace sheenlet-core ts && yarn workspace ui ts

lint:
	yarn workspace sheenlet-app lint && yarn workspace sheenlet-core lint && yarn workspace ui lint

test:
	yarn workspace sheenlet-core jest && yarn workspace ui jest

jest:
	yarn workspace sheenlet-core jest && yarn workspace ui jest
