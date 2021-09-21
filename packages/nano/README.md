# `nano`

> For a short description of how to run the example please check
> [README.md](../../README.md) in the repo root folder or
> <https://github.com/andreygrechin/nano/blob/main/README.md>

## YANG model

A tree representation of the service without NSO inherited nodes.

```text
module: example-nano
  +--rw nano
     +--rw nano* [id]
     |  +--rw notify
     |  |  +---x notify-approver
     |  +--rw tests
     |  |  +---x pre-test
     |  |  +---x post-test
     |  +--rw id                             string
     |  +--rw device                         -> /ncs:devices/device/name
     |  +--rw name-server?                   string
     |  +--rw approved?                      boolean
     +--rw sla
        +--rw timeouts
        |  +---x timeout
        |  +--rw jeopardy?    uint32
        |  +--rw violation?   uint32
        +--rw webex
        |  +--rw room-id?         string
        |  +--rw bot-token?       string
        |  +---x send-test-msg
        +---x init-sla-policy
           +---w input
           +--ro output
```

## YANG linting

`pyang` shows some false positives related to refines and alignments of
different parts of models. So, it will be better to use `yanger` which is a tool
written in Erlang by Martin Bjorklund, original author of `pyang`.

`yanger` is available as part of an NSO installation or as
[a separate tool](https://github.com/mbj4668/yanger). Hopefully, you will be
surprised by a dramatic increase in performance while working with big YANG
models.
