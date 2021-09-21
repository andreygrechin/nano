#
# The 'lux' test tool can be obtained from:
#
#   https://github.com/hawk/lux.git
#

# Make sure the TARGET_DIR has got the following make targets:

export TARGET_DIR=../../../..

.PHONY: all
all: test

.PHONY: test
test:
	lux run.lux

.PHONY: clean
clean:
	$(MAKE) -C $(TARGET_DIR) clean

.PHONY: build
build:
	$(MAKE) -C $(TARGET_DIR) build

.PHONY: start
start:
	$(MAKE) -C $(TARGET_DIR) start

.PHONY: stop
stop:
	$(MAKE) -C $(TARGET_DIR) stop
