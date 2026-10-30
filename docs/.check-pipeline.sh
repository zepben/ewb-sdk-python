#!/usr/bin/env bash
# version 1.1

# Remove @ from the DOCKER command, we are not Makefile
# Shouldn't be needed for Makefile 1.1 and above, let's keep it 
# until that's everywhere
DOCKER=$(echo $DOCKER | sed -e "s/\@//g")

org=$(echo "${PIPELINE}" | cut -f1 -d\/)

if [ "$org" == "local" ]; then
    # must be running tests on local stuff, no need to fetch image
    exit 0
fi

repo=$(echo "${PIPELINE}" | cut -f2 -d\/)
registry="https://hub.docker.com/v2/namespaces/$org/repositories/$repo/tags?platforms=true&page_size=10&page=1&ordering=last_updated&name=latest"

local_shas=$(${DOCKER} inspect "${PIPELINE}" | jq '.[].RepoDigests' | sed -e "s/\"//g")
remote_sha=$(curl -s "$registry" | jq '.results[].digest' | sed -e "s/\"//g")

update="yes" 
for sha in $local_shas; do 
    if [[ "$sha" =~ "$remote_sha" ]]; then 
        update="no"; 
    fi
done 

if [[ "$update" == "yes" ]]; then 
    echo
    echo "Downloading latest pipeline-docusaurus container"
    echo 
    ${DOCKER} pull "${PIPELINE}"
fi
