PACKAGES = nano

PY_FOLDERS = packages/nano/python/nano_helper
PY_FOLDERS_TESTS = packages/nano/python/nano_helper

.PHONY: all
all: clean build start

include make-python.mk

.PHONY: build
build: compile netsim ncs-setup

.PHONY: clean
clean: stop cleanncs

.PHONY: reload
reload: compile
	./tools/pkgreload.sh

.PHONY: stop
stop:
	@printf -- "\n\033[33;1m>>> Stoping NCS... \033[0m\n"
	-ncs --stop
	-ncs-netsim stop --dir netsim

.PHONY: compile
compile:
	@printf -- "\n\033[33;1m>>> Compiling YANG models... \033[0m\n"
	@for pkg in $(PACKAGES) ; do \
		printf -- "\033[36;1mCompiling $$pkg... \033[0m \n"; \
		$(MAKE) -C "packages/$$pkg/src/" clean all || exit 1; \
	done

.PHONY: reset
reset:
	@printf -- "\n\033[33;1m>>> Resetting NCS configuration... \033[0m\n"
	ncs --stop
	rm -fr ./ncs-cdb/*.cdb
	ncs

.PHONY: netsim
netsim:
	@printf -- "\n\033[33;1m>>> Creating netsim network... \033[0m\n"
	ncs-netsim create-network cisco-ios-cli-3.8 2 r
	@for package in $(PACKAGES) ; do \
		printf -- "\033[37;1m$$package... \033[0m \n"; \
		if [ -d packages/$$package/netsim ]; then \
			$(MAKE) -C "packages/$$package/netsim" netsim || exit 1; \
		fi; \
	done
	ncs-netsim ncs-xml-init > configs/netsim-init.xml

.PHONY: ncs-setup
ncs-setup:
	@printf -- "\n\033[33;1m>>> Setting up NCS... \033[0m\n"
	ncs-setup --netsim-dir ./netsim --dest .
	@printf -- "\033[36;1mCoping configs... \033[0m \n"
	cp -v configs/*.xml ncs-cdb/
	python3 tools/update_ncsconf.py

.PHONY: cleanncs
cleanncs:
	@printf -- "\n\033[33;1m>>> Cleaning up... \033[0m \n"
	@for pkg in $(PACKAGES) ; do \
		printf -- "\033[36;1mCleaning up $$pkg... \033[0m \n"; \
		$(MAKE) -C "packages/$$pkg/src/" clean || exit 1; \
	done
	@printf -- "\033[36;1mDeleting ncs-setup folders and files... \033[0m \n"
	rm -rf ./logs ./ncs-cdb ./netsim ./scripts ./state ./target ./.ipython ./Library
	rm -rf ./packages/cisco-ios-cli-3.8
	rm -fr ncs.conf README.ncs README.netsim storedstate
	@printf -- "\033[36;1mDeleting lux logs... \033[0m \n"
	@find ./tests -type d -name "lux_logs" -exec rm -fr {} \; || exit 0

.PHONY: start
start:
	ncs-netsim start
	ncs
	./tools/sync-from.sh
	@printf -- "\n\033[32;1mUse 'make cli' or 'make webui' for accessing NSO. \033[0m\n"
	@printf -- "\n\033[32;1mUse 'make nsotest' for running tests. \033[0m\n"

.PHONY: startint
startint:
	@printf -- "\n\033[33;1m>>> Starting NCS interactively.. \033[0m \n"
	@printf -- "\n\033[32;1mUse ctrl-d to gracefully exit. \033[0m\n"
	-ncs --stop
	ncs --foreground --verbose --stop-on-eof

.PHONY: cli
cli:
	ncs_cli -C -u admin

# for testing NACM rules, because a default console connection skips checks
.PHONY: cli-en
cli-en:
	ssh engineer@0.0.0.0 -p 2024 -o PreferredAuthentications=password -o PasswordAuthentication=yes -o PubkeyAuthentication=no

# for testing NACM rules, because a default console connection skips checks
.PHONY: cli-app
cli-app:
	ssh approver@0.0.0.0 -p 2024 -o PreferredAuthentications=password -o PasswordAuthentication=yes -o PubkeyAuthentication=no

.PHONY: webui
webui:
	open http://0.0.0.0:8080/login.html

.PHONY: logs
logs:
	tail -f -n0 ./logs/*.log

.PHONY: traces
traces:
	tail -f -n0 ./logs/*.trace

.PHONY: backupncs
backupncs:
	./tools/backup-ncs.sh

.PHONY: lint-yanger
lint-yanger:
	@printf -- "\n\033[33;1m>>> Linting YANG models with yanger... \033[0m\n"
	@for pkg in $(PACKAGES) ; do \
		printf -- "\033[36;1mLinting $$pkg... \033[0m \n"; \
		./tools/lint-yanger.sh packages/$$pkg || echo "failed, continue..."; \
	done

.PHONY: lint-pyang
lint-pyang:
	@printf -- "\n\033[33;1m>>> Linting YANG models with pyang... \033[0m\n"
	@for pkg in $(PACKAGES) ; do \
		printf -- "\033[36;1mLinting $$pkg... \033[0m \n"; \
		./tools/lint-pyang.sh packages/$$pkg || echo "failed, continue..."; \
	done

.PHONY: nsotest
nsotest:
	$(MAKE) -C tests test || exit 1
