+++
title = "lark"
chapter = false
weight = 5
+++

## Overview
This C2 profile consists of a server which listens for the im.message.reaction.created_v1 Lark event. 

On receiving a GLANCE reaction, indicating a new message from the agent, the server fetches the message's body content which is a file ID, downloads the file, then forwards the file contents to the Mythic server via the standard REST API. It then takes the response, uploads it to Feishu drive as a file, and updates the corresponding message with a title of TASK and the body containing the new file ID.

On receiving a SMILE reaction, indicating the agent has succesfully received the task, the server deletes the corresponding file from Feishu drive.
 

### Lark C2 Workflow
{{<mermaid>}}
sequenceDiagram
    participant M as Mythic
    participant L as Lark Container
    participant O2 as open.feishu.cn
    participant H as Lark Chat
    participant O1 as open.feishu.cn
    participant A as Agent
    A ->>+ O1: Agent calls API to upload message <br/> as file to Feishu drive
    O1 -->>- A: Feishu returns file ID
    A ->>+ O1: Agent calls API to send message card <br/> containing the file ID as content
    O1 ->> H: Feishu API sends message <br/> card to group chat
    O1 -->>- A: Feishu returns message ID
    A ->>+ O1: Agent calls API to add GLANCE <br/> reaction to message ID
    O1 ->>+ H: Feishu API adds GLANCE emoji <br/> to message
    O2 ->>+ L: Feishu sends event to webhook <br/> containing message ID and emoji
    L ->>+ O2: Container calls API to retrieve <br/> message contents
    O2 -->>- L: Feishu returns message contents <br> (file ID)
    L ->>+ O2: Container calls API to download file ID
    O2 -->>- L: Feishu returns file contents <br/> (agent message)
    L ->>+ O2: Container calls API to delete file ID
    L ->>+ M: Container forwards message <br/> to Mythic
    M -->>- L: Mythic returns tasking
    L ->>+ O2: Container calls API to upload message <br/> as a file to Feishu drive
    O2 -->>- L: Feishu returns file ID
    L ->>+ O2: Container calls API to update message <br/> card content with file ID and title <br/> with "TASK"
    O2 ->>+ H: Feishu API updates message <br/> card contents and title
    A ->>+ O1: Agent calls API to retrieve message <br/> contents
    O1 -->>- A: Feishu returns message contents <br/> (file ID)
    A ->>+ O1: Agent calls API to download file ID
    O1 -->>- A: Feishu returns file contents <br/> (tasking)
    A ->>+ O1: Agent calls API to add SMILE <br/> reaction to message indicating <br/> the task has been received <br/> and the file can be deleted
    O1 ->>+ H: Feishu API adds SMILE emoji <br/> to message
    O2 ->>+ L: Feishu sends event to webhook <br/> containing message ID and emoji
    L ->>+ O2: Container calls API to retrieve <br/> message contents
    O2 -->>- L: Feishu returns message contents <br> (file ID)
    L ->>+ O2: Feishu calls API to delete file ID
{{< /mermaid >}}

## Configuration Options
The profile reads a `config.json` file for the required Lark bot credentials, event subscription token, and port to listen on.

```JSON
{
  "lark_groupchat_name": "",
  "lark_app_id": "",
  "lark_app_secret": "",
  "lark_verification_token": "",
  "lark_encrypt_key": "",
  "port": "80"
}
```

- lark_groupchat_name -> The groupchat in which the agent and server will send messages and communicate
- lark_app_id -> The application ID of the Lark bot being used for C2 communications
- lark_app_secret -> The secret of the Lark bot being used for C2 communications
- lark_verification_token -> The verification token of the Lark bot being used to handle event subscriptions
- lark_encrypt_key -> The encryption key of the Lark bot being used to encrypt event subscription messages
- port -> The port the event subscription webhook will listen on

### Profile Options
#### Lark Groupchat Name
The groupchat in which the agent and server will send messages and communicate

#### Lark App ID
The application ID of the Lark bot being used for C2 communications

#### Lark App Secret
The secret of the Lark bot being used for C2 communications

#### Crypto Type
Indicate if you want to use no crypto (i.e. plaintext) or if you want to use Mythic's aes256_hmac. Using no crypto is really helpful for agent development so that it's easier to see messages and get started faster, but for actual operations you should leave the default to aes256_hmac.

#### Callback Interval
A number to indicate how many seconds the agent should wait in between tasking requests.

#### Callback Jitter
Percentage of jitter effect for callback interval.

#### Kill Date
Date for the agent to automatically exit, typically the after an assessment is finished.

#### Perform Key Exchange
T or F for if you want to perform a key exchange with the Mythic Server. When this is true, the agent uses the key specified by the base64 32Byte key to send an initial message to the Mythic server with a newly generated RSA public key. If this is set to `F`, then the agent tries to just use the base64 of the key as a static AES key for encryption. If that key is also blanked out, then the requests will all be in plaintext.


## OPSEC
This profile calls the same Feishu APIs in sequence and should be taken into consideration for profiling analytics. Consider customizing the profile to use alternative reaction types, and call other Feishu APIs between legitimate calls to break the upload, send, download, reaction call pattern.

## Development

All of the code for the server is Python3 using `Sanic` and located in `C2_Profiles/lark/c2_code/server`.
