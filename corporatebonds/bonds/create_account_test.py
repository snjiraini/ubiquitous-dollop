import sys  # For printing errors with traceback

def generateHederaAccount():
    from hedera import (
        Hbar,
        PrivateKey,
        AccountCreateTransaction,
    )
    from get_client import client

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

generateHederaAccount()