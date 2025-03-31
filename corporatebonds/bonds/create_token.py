import sys  # For printing errors with traceback
import os
import json
from dotenv import load_dotenv
from hedera import AccountId, PrivateKey, Client

def generateBondToken(token_name, token_symbol, initial_supply):
    from hedera import (
        TokenCreateTransaction,
        TokenType,
        TokenSupplyType,
        Hbar,
        PrivateKey
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
        # Create a Bond Token
        txn = (
            TokenCreateTransaction()
            .setTokenName(token_name)
            .setTokenSymbol(token_symbol)
            .setTokenType(TokenType.FUNGIBLE_COMMON)  # Fungible for bonds
            .setSupplyType(TokenSupplyType.FINITE)  # ✅ Fix: Must be explicitly set
            .setMaxSupply(initial_supply)  # ✅ Fix: Only valid if SupplyType = FINITE
            .setDecimals(0)  # No decimal places
            .setTreasuryAccountId(OPERATOR_ID)  # The treasury holds initial supply
            .setAdminKey(OPERATOR_KEY.getPublicKey())
            .setSupplyKey(OPERATOR_KEY.getPublicKey())  # Allows minting/burning
            .setInitialSupply(0)  # Start with 0 tokens
            .setFreezeDefault(False)  # No automatic freezing
            .freezeWith(client)
            .sign(OPERATOR_KEY)
            .execute(client)
        )

        # Get the token ID from the receipt
        receipt = txn.getReceipt(client)
        token_id = receipt.tokenId.toString()  # ✅ Convert Token ID to string

        print(f"✅ Bond Token Created! Token ID: {token_id}")
        return {
            "Tokenid": receipt.tokenId.toString()
        }

    except Exception as e:
        print(f"❌ Error creating bond token: {str(e)}")
        print(str(e), file=sys.stderr)
        import traceback
        traceback.print_exc()  # Print full stack trace

        return {
            "error": "Failed to generate Hedera Bond Token.",
            "details": str(e),
        }
