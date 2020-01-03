import os

SMTP_REPLY_CODE_OK = 250
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SCHEMA_PATH = os.path.join(SCRIPT_DIRECTORY, 'jsons', 'schema.json')
TALOS_ADDRESS = 'https://www.talosintelligence.com/reputation_center/lookup?search='
# Possible implementation enhacement, put json reason codes in a structure, in a file named 'api codes' or something like that, e.g. MX_FETCH_FAIL='MX_FETCH_FAIL'. bloats code but insures tight api.