DIRS = lux

.PHONY: all
all: test

.PHONY: test
test:
	@for d in $(DIRS) ; do \
	  $(MAKE) -C $$d test || exit 1; \
	done

.PHONY: clean
clean:
	@for d in $(DIRS) ; do \
	  $(MAKE) -C $$d clean || exit 1; \
	done

.PHONY: build
build:
	@for d in $(DIRS) ; do \
	  $(MAKE) -C $$d build || exit 1; \
	done

.PHONY: start
start:
	@for d in $(DIRS) ; do \
	  $(MAKE) -C $$d start || exit 1; \
	done

.PHONY: stop
stop:
	@for d in $(DIRS) ; do \
	  $(MAKE) -C $$d stop || exit 1; \
	done
