import dotenv from "dotenv";
import { Client, TransferTransaction, AccountId, PrivateKey } from "@hashgraph/sdk";

dotenv.config();

// Load Hedera credentials
const operatorId = AccountId.fromString(process.env.OPERATOR_ID);
const operatorKey = PrivateKey.fromString(process.env.OPERATOR_KEY);
const tokenId = process.env.TOKEN_ID;

// Connect to Hedera Testnet
const client = Client.forTestnet().setOperator(operatorId, operatorKey);

// List of recipients and amounts (Replace with actual addresses)
const recipients = [
    { account: "0.0.123456", amount: 10 }, // Investor 1
    { account: "0.0.654321", amount: 20 }, // Investor 2
    { account: "0.0.987654", amount: 15 }  // Investor 3
];

/**
 * 🚀 Batch Transfer Tokens to Multiple Addresses
 */
async function batchTransferTokens() {
    console.log("🚀 Initiating batch token transfer...");

    const tx = new TransferTransaction();

    // Subtract tokens from the sender (Treasury)
    tx.addTokenTransfer(tokenId, operatorId, -recipients.reduce((sum, r) => sum + r.amount, 0));

    // Add token transfers to each recipient
    recipients.forEach(({ account, amount }) => {
        tx.addTokenTransfer(tokenId, AccountId.fromString(account), amount);
    });

    // Execute transaction
    const signedTx = await tx.freezeWith(client).sign(operatorKey);
    const response = await signedTx.execute(client);
    const receipt = await response.getReceipt(client);

    console.log(`✅ Batch Transfer Successful! Transaction ID: ${response.transactionId}`);
    console.log(`🔗 View on HashScan: https://hashscan.io/testnet/transaction/${response.transactionId}`);
}

batchTransferTokens().catch(console.error);
