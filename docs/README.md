# Docs with Docusaurus 3

## Requirements:
- make
- container utility (tested with `docker` and `podman`)

> NOTE: on Windows, it's highly recommended to use WSL to build docs. Look for `Windows` notes below

## TLDR;

- To build, run `make build` in `docs` folder of your repository. The default build is using `docker`, if you want to use `podman`, run
```bash
export DOCKER=@podman
```
before running any make command.

- To serve the project to see the site is fine, run `make serve` after building.
- To live-serve while working, run `make start`.
- To clean things and start over, run `make clean`.


# Details

## Layout

This is a docs layout that is utilised by Docusaurus (and our CI) to build static documentation. The layout is as follows:

- docs (where the `next` version content lives)
- archive (where the previous versions live)
- site-config (where the sidebar and release-notes.md reside and where the actual build happens)
- Makefile for convenient work flows
- README

As per usual, edit docs in the `docs` folder, and update the sidebar if you need to in `site-config` folder.

## How it works

The heart of the build is in the `pipeline-docusaurus` pipeline container. It includes all the templates needed to create a Docusaurus website, 
and those templates, populated, are placed into the site-config directory for the build. These include `package.json`, `package-lock.json`, as well
as docusarus configuration. Additionally, cached `node-modules` are linked for the build purposes.

This makes out-of-container builds complicated, as such builds within the container are always recommended.

### How to build

To build the docs site, one need to run a script within a container that does all the work. It is highly recommended to just use make commands that
run the container with all the required options. In general though, the following is performed:

- The 'current' (docs folder of the repository) is mounted in the container as `/docs`
- The templates are copied over from /templates into the `/docs/site-config` and populated appropriately
- The `/node-modules` is linked inside `/docs/site-config`
- The `/docs/docs` is mounted inside `/docs/site-config`
- The local `.npmrc` is linked inside `/docs/site-config`
- The build is run in the `/docs/site-config` directory

### Windows notes

If you work on your project on Windows file system, and you only need to work on the docs once in a while, it's recommended to setup WSL, 
install `make` and `docker/podman`, and perform builds directly on the Windows mount point (i.e. something like `/mnt/c/...`). However, these
builds will be somewhat slow, which might be okay for a now-and-then use cases. The reason is that the mount (`/mnt/c`) is actually network-simulated, and
to build, npm will need to "fetch" all it needs via this network simulation. Additionally, using `npm start` for live-reload will not work, as this combination
does not support `inotify` functionality, hence live reload will not see the changed files.

If you need faster builds, and work a lot with the documentation, and work often with the live-reload feature (`npm start`), the alternative is to actually
copy the project into the local WSL environment (for example, `/home/alex/...` on you WSL installation), and run all the builds in that environment. The documentation edits
are still possible with any Windows tool via the reverse network mount (SMB, `\\wsl$\<Linux>\home\alex\...`), but the benefit of this is the speed of the builds, and the ability
to `watch` filesystem changes, which are not possible in the first option.


