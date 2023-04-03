from mythic_c2_container.C2ProfileBase import *


class Lark(C2Profile):
    name = "lark"
    description = "Leverages lark/feishu bots for C2 communications"
    author = "@nick_frischkorn"
    is_p2p = False
    is_server_routed = False
    parameters = [
        C2ProfileParameter(
            name="lark_groupchat_name",
            description="Name of the groupchat the Lark bot will communicate in",
            default_value="",
            required=True,
        ),
        C2ProfileParameter(
            name="lark_app_id",
            description="App ID of the Lark bot used for C2 communications",
            default_value="",
            required=True,
        ),
        C2ProfileParameter(
            name="lark_app_secret",
            description="Secret of the Lark bot used for C2 communications",
            default_value="",
            required=True,
        ),
        C2ProfileParameter(
            name="killdate",
            description="Kill Date",
            parameter_type=ParameterType.Date,
            default_value=365,
            required=False,
        ),
        C2ProfileParameter(
            name="encrypted_exchange_check",
            description="Perform Key Exchange",
            choices=["T", "F"],
            required=False,
            parameter_type=ParameterType.ChooseOne,
        ),
        C2ProfileParameter(
            name="callback_jitter",
            description="Callback Jitter in percent",
            default_value="23",
            verifier_regex="^[0-9]+$",
            required=False,
        ),
        C2ProfileParameter(
            name="AESPSK",
            description="Crypto type",
            default_value="aes256_hmac",
            parameter_type=ParameterType.ChooseOne,
            choices=["aes256_hmac", "none"],
            required=False,
            crypto_type=True
        ),
        C2ProfileParameter(
            name="callback_interval",
            description="Callback Interval in seconds",
            default_value="20",
            verifier_regex="^[0-9]+$",
            required=False,
        ),
    ]
