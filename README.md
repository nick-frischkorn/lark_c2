# Lark

## Overview

**This profile is supported by:** https://github.com/nick-frischkorn/lark_poseidon

This is a Mythic C2 Profile called lark. It provides a way for agents to communicate via Feishu APIs. This profile supports:

* Kill Dates
* Sleep Intervals
* Message Encryption

The c2 profile has `mythic_c2_container==0.0.23` PyPi package installed and reports to Mythic as version "4". 

## How To Install

- `sudo ./mythic-cli install github https://github.com/nick-frischkorn/lark_c2`

- `sudo ./mythic-cli install folder /path/to/lark/`

See https://docs.mythic-c2.net/installation#installing-agents-c2-profiles for more information

## Lark C2 Workflow

```mermaid
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
```

## Configuring The Profile Container

The C2 profile handles configuration using a `config.json` file which can be modified within the Mythic instance. It contains 6 parameters:

- lark_groupchat_name
- lark_app_id
- lark_app_secret
- lark_verification_token
- lark_encrypt_key
- port

Browse to C2 Profiles, then click on the dropdown arrow next to `Start Profile`, then click `View/Edit Config` to change the above values.

## Lark C2 Profile Setup

1. Sign in to larksuite and browse to https://open.larksuite.com/app?lang=en-US

2. Select `Custom Apps`, then `Create Custom App`

    <img src="images/1.png">

3. Choose a name and description, then select `Create`

    <img src="images/2.png" width="400">

4. Select `Add Features` on the left hand panel, then select `By Feature`, then select `Add` under `Bot`

    <img src="images/3.png">

5. Select `Permissions & Scopes` on the left hand panel, then add the `im:chat`, `im:message`, `drive:file`, and `drive:drive` scopes, and select `Add in bulk`

    <img src="images/4.png">

6. Select `Confirm and go to create app version`, then select `Create a version`

    <img src="images/5.png" width=400>

    <img src="images/6.png">

7. Fill out the version details, then select `Save`

    <img src="images/7.png" width=400>

8. Select `Submit for release`

    <img src="images/8.png">

9. The Open Platform Assistant will send you a message within your larksuite tenant, select `Admin Console` to navigate to the review page

    <img src="images/9.png" width=400>

10. Select `Review` next to your bot, then `Approve`

    <img src="images/10.png">

11. Create a groupchat within Lark, select `Settings`, then select `Bots`, then select `Add Bot` and choose your Lark bot

    <img src="images/11.png" width=400>

12. Navigate back to the developer console and select `Credentials & Basic Info` on the left hand panel and copy your `App ID` and `App Secret`

    <img src="images/12.png">

13. Select `Event Subscriptions` on the left hand panel and copy your `Verification Token` 

    <img src="images/15.png">

14. Within Mythic, update lark's C2 profile with your obtained `Verification Token`, `App ID`, `App Secret`, and the name of the groupchat you added the bot to, then start the profile.

15. Navigate back to the `Event Subscriptions` panel, configure the `Request URL` to point to Mythic's IP and `port` from the config file, then select `Save`

    <img src="images/13.png">

16. Once the `Request URL` has received the verification event, select `Add Events`, then select `reaction.created`

    <img src="images/14.png">

## To Do

- Upgrade server to be async + support HTTPS
- Add Lark event encryption option
- Add agent file upload/download capabilities
- Add command to switch to regular HTTP beaconing
