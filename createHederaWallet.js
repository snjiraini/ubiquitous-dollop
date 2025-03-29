import "dotenv/config"; // Automatically loads .env variables
import { Client, PrivateKey, AccountCreateTransaction, Hbar } from "@hashgraph/sdk";

// Retrieve credentials from .env
const operatorId = process.env.OPERATOR_ID;
const operatorKey = process.env.OPERATOR_KEY;

if (!operatorId || !operatorKey) {
    throw new Error("❌ Missing HEDERA_OPERATOR_ID or HEDERA_OPERATOR_KEY in .env file");
}

/**
 * Create a Hedera Testnet Wallet Address.
 * @returns {Promise<{ accountId: string, privateKey: string, publicKey: string }>}
 */
export async function createHederaWallet() {
    try {
        // Connect to Hedera Testnet
        const client = Client.forTestnet();
        client.setOperator(operatorId, operatorKey);

        // Generate new wallet keys
        const newPrivateKey = PrivateKey.generateED25519();
        const newPublicKey = newPrivateKey.publicKey;

        // Create new Hedera account
        const transaction = new AccountCreateTransaction()
            .setKey(newPublicKey)
            .setInitialBalance(new Hbar(1));

        // Execute transaction
        const response = await transaction.execute(client);
        const receipt = await response.getReceipt(client);
        const newAccountId = receipt.accountId.toString();

        console.log(`✅ New Hedera Wallet Created: ${newAccountId}`);
        return {
            accountId: newAccountId,
            privateKey: newPrivateKey.toStringRaw(),
            publicKey: newPublicKey.toStringRaw()
        };
    } catch (error) {
        console.error("❌ Error creating Hedera Wallet:", error);
        return null;
    }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
    createHederaWallet().then(wallet => console.log(wallet));
}
