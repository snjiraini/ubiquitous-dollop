import sys  # For printing errors with traceback
import os
import json
from dotenv import load_dotenv
from hedera import AccountId, PrivateKey, Client

def generateHederaAccount():
    from hedera import (
        Hbar,
        PrivateKey,
        AccountCreateTransaction,
    )
    load_dotenv()

    if "HEDERA_CONFIG_FILE" in os.environ:
        client = Client.fromConfigFile(os.environ["HEDERA_CONFIG_FILE"])
        OPERATOR_ID = client.operatorAccountId
        with open(os.environ["HEDERA_CONFIG_FILE"]) as f:
            OPERATOR_KEY = PrivateKey.fromString(json.load(f)["operator"]["privateKey"])

    else:
        if "OPERATOR_ID" not in os.environ or "OPERATOR_KEY" not in os.environ:
            exit("Must set OPERATOR_ID OPERATOR_KEY environment variables")
        OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
        OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])
        HEDERA_NETWORK = os.environ.get("HEDERA_NETWORK", "testnet")
        if HEDERA_NETWORK == "previewnet":
            client = Client.forPreviewnet()
        elif HEDERA_NETWORK == "testnet":
            client = Client.forTestnet()
        else:
            client = Client.forMainnet()
        client.setOperator(OPERATOR_ID, OPERATOR_KEY)

    try:
        # Generate an Ed25519 private/public key pair
        newKey = PrivateKey.generate()
        newPublicKey = newKey.getPublicKey()

        # Print the generated keys to the terminal
        print(f"🔑 Private Key: {newKey.toString()}")
        print(f"🔓 Public Key: {newPublicKey.toString()}")

        # Create a new Hedera account with the generated public key
        tran = AccountCreateTransaction()
        resp = tran.setKey(newPublicKey).setInitialBalance(Hbar(2)).execute(client)
        receipt = resp.getReceipt(client)

        # Print the account ID to the terminal
        print(f"✅ Hedera Account Created: {receipt.accountId.toString()}")

        return {
            "accountid": receipt.accountId.toString(),
            "publickey": newPublicKey.toString(),
            "privatekey": newKey.toString(),
        }

    except Exception as e:
        # Print detailed error information to the terminal
        print("❌ Error generating Hedera account:", file=sys.stderr)
        print(str(e), file=sys.stderr)
        import traceback
        traceback.print_exc()  # Print full stack trace

        return {
            "error": "Failed to generate Hedera account.",
            "details": str(e),
        }
