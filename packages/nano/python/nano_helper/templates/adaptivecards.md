# Adaptive Card

## References

- <https://developer.webex.com/docs/api/guides/cards>
- <https://developer.webex.com/buttons-and-cards-designer>
- <https://adaptivecards.io/explorer/>
- <https://adaptivecards.io/schemas/adaptive-card.json>

## API errors

Webex API may return some errors on validation of Adaptive Card JSONs, see
below. However, a schema validation and specification checks are seemed OK.

```json
"errors": {
    "attachments": {
        "code": "invalid_attachments",
        "reason": "Invalid Adaptive Card Json",
        "attachmentErrors": [
            "#/body/5: required key [text] not found",
            "#/body/5: required key [id] not found",
            "#/body/5: required key [title] not found",
            "#/body/5: required key [id] not found",
            "#/body/5: extraneous key [horizontalAlignment] is not permitted",
            "#/body/5: required key [id] not found",
            "#/body/5: extraneous key [horizontalAlignment] is not permitted",
            "#/body/5: required key [id] not found",
            "#/body/5: extraneous key [horizontalAlignment] is not permitted",
            "#/body/5: required key [id] not found",
            "#/body/5: extraneous key [horizontalAlignment] is not permitted",
            "#/body/5: required key [id] not found",
            "#/body/5: required key [choices] not found",
            "#/body/5: required key [images] not found",
            "#/body/5: required key [url] not found",
            "#/body/5: required key [facts] not found",
            "#/body/5: required key [items] not found",
            "#/body/5: extraneous key [style] is not permitted"
        ]
    }
}
```
