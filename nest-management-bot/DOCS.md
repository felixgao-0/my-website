# Nest Management Bot
Websocket Docs

wip docs, all items inside are subject to change. Some doc items are for whats planned and haven't been fully implemented yet


## Websocket Docs
### Message Syntax
All messages have a status and message:
```json
{
  "status": "info",
  "message": "example message to send"
}
```

The following are valid status types:
- `info`
- `command`
- `command_response`
- `warning`
- `error`

Command responses and commands can also include a payload item with anything inside:
```json
{
  "status": "command_response",
  "message": "response_download_raid_shadow_legends",
  "payload": {
    "success": false,
    "reason": "I skipped the sponsor segment lol"
  }
}
```
Commands may have a payload in cases where more specific info is needed
```json
{
  "status": "command",
  "message": "obtain_process_info",
  "payload": {
    "pid": "43235" // PID of process to manage
  }
}
```

Commands can have the following message text:
- `obtain_global_info`
- `obtain_all_process_info`
- `obtain_process_info`
- `kill_process`
- `restart_process`*
- `start_process`*

*Makes use of systemd

### Connecting:
To connect fully, the client needs to send the following message
```json
{
  "version": "0.1.0a"
  // Client version, used to avoid issues with old code
}
```

The server will verify the data sent and then either disconnect the client if the data is incorrect, or keep the connection and send back the following:
```json
{
  "status": "info",
  "message": "Authenticated :D"
}
```