def modal():
    return {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Nest Management Bot",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Bye Bye!",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*View your Processes:*"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Slack Bot"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Manage Process",
                        "emoji": True
                    },
                    "value": "pid232",
                    "action_id": "manage-process"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Caddy"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Manage Process",
                        "emoji": True
                    },
                    "value": "pid1",
                    "action_id": "manage-process"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Made by Felix with open-source :sparkling_heart:",
                        "emoji": True
                    }
                ]
            }
        ]
    }