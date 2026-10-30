DOCKER?=@docker
PIPELINE=zepben/pipeline-docusaurus
REPO=-e REPO_NAME=$(shell basename $(shell git rev-parse --show-toplevel 2>/dev/null))


all: build

.PHONY: build
build:
	${DOCKER} run --rm -v $(shell pwd):/docs -v ~/.npmrc:/root/.npmrc ${REPO} -it ${PIPELINE} /templates/build.sh
	@echo 
	@echo "#############################################################"
	@echo "# The build has finished; as the result files are not here, #" 
	@echo "# use 'make serve' command to test your build locally       #"
	@echo "#############################################################"
	@echo

start:
	${DOCKER} run --rm -v $(shell pwd):/docs -p 3000:3000 -v ~/.npmrc:/root/.npmrc ${REPO} -it ${PIPELINE} /templates/run.sh start

serve:
	${DOCKER} run --rm -v $(shell pwd):/docs -p 3000:3000 -v ~/.npmrc:/root/.npmrc ${REPO} -it ${PIPELINE} /templates/run.sh serve

# Run clean in the container so that there's no issue with permissions
clean:
	${DOCKER} run --rm -v $(shell pwd):/docs ${PIPELINE} sh -c "cd /docs/site-config; rm -rf docs node_modules src versioned_docs version* tsconfig.json package* docusaurus.config.js build run.sh"
