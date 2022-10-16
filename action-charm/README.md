# action-charm

A charm that demonstrates how to implement an action for a charm.

Read more on actions here: https://juju.is/docs/sdk/actions

## Usage
Build the charm

    charmcraft pack

Deploy it:
    juju add-model mytestmodel
    juju deploy ./action-charm_ubuntu-22.04-amd64.charm  

Run the action:

    $ juju run-action action-charm/0  hello message="Hello world" 
    Action queued with id: "6"
    
Show the action output:

    $ juju show-action-output 6
    UnitId: action-charm/0
    id: "6"
    log:
    - 2022-10-16 15:49:07 +0200 CEST Hello world
    results:
    the-message: Hello world
    status: completed
    timing:
    completed: 2022-10-16 13:49:08 +0000 UTC
    enqueued: 2022-10-16 13:49:05 +0000 UTC
    started: 2022-10-16 13:49:07 +0000 UTC