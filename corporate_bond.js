import dotenv from "dotenv";
import { 
    Client, 
    TokenCreateTransaction, 
    TokenType, 
    TokenSupplyType, 
    TransferTransaction, 
    AccountId, 
    PrivateKey, 
    Hbar 
} from "@hashgraph/sdk";

dotenv.config();

// Load environment variables
const operatorId = AccountId.fromString(process.env.OPERATOR_ID);
const operatorKey = PrivateKey.fromString(process.env.OPERATOR_KEY);

// Connect to Hedera
const client = Client.forTestnet().setOperator(operatorId, operatorKey);

// The token ID will be assigned after creation
let bondTokenId = null;

/**
 * Step 1: Create the Corporate Bond Token
 */
async function createBondToken() {
    console.log("Creating Corporate Bond Token...");
    const tx = new TokenCreateTransaction()
        .setTokenName("Corporate Bond 2025")
        .setTokenSymbol("CB2025")
        .setTokenType(TokenType.FungibleCommon)
        .setDecimals(0) // Each token represents 1 bond
        .setInitialSupply(1000) // Issuing 1000 bonds
        .setTreasuryAccountId(operatorId)
        .setSupplyType(TokenSupplyType.Finite)
        .setMaxSupply(1000) // Maximum supply is 1000 bonds
        .freezeWith(client);

    const signTx = await tx.sign(operatorKey);
    const txResponse = await signTx.execute(client);
    const receipt = await txResponse.getReceipt(client);
    bondTokenId = receipt.tokenId;

    console.log(`✅ Corporate Bond Token Created: ${bondTokenId}`);
}

/**
 * Step 2: Distribute Bonds to Investors
 */
async function distributeBonds(investorId, amount) {
    console.log(`Distributing ${amount} bonds to Investor ${investorId}...`);
    const tx = new TransferTransaction()
        .addTokenTransfer(bondTokenId, operatorId, -amount) // Deduct from Treasury
        .addTokenTransfer(bondTokenId, AccountId.fromString(investorId), amount) // Send to Investor
        .freezeWith(client);

    const signTx = await tx.sign(operatorKey);
    const txResponse = await signTx.execute(client);
    const receipt = await txResponse.getReceipt(client);
    console.log(`✅ Transferred ${amount} bonds to ${investorId}`);
}

/**
 * Step 3: Pay Coupon Interest to Investors
 */
async function payCoupon(investorId, amount) {
    console.log(`Paying ${amount} HBAR coupon to Investor ${investorId}...`);
    const tx = new TransferTransaction()
        .addHbarTransfer(operatorId, new Hbar(-amount))
        .addHbarTransfer(AccountId.fromString(investorId), new Hbar(amount))
        .freezeWith(client);

    const signTx = await tx.sign(operatorKey);
    const txResponse = await signTx.execute(client);
    const receipt = await txResponse.getReceipt(client);
    console.log(`✅ Paid ${amount} HBAR to ${investorId} as interest.`);
}

/**
 * Step 4: Redeem Bonds at Maturity
 */
async function redeemBond(investorId, amount) {
    console.log(`Redeeming ${amount} bonds for Investor ${investorId}...`);
    const redemptionPrice = 100; // Assuming each bond is worth 100 HBAR

    const tx = new TransferTransaction()
        .addTokenTransfer(bondTokenId, AccountId.fromString(investorId), -amount) // Investor returns bonds
        .addTokenTransfer(bondTokenId, operatorId, amount) // Treasury receives bonds
        .addHbarTransfer(operatorId, new Hbar(-amount * redemptionPrice)) // Pay investor
        .addHbarTransfer(AccountId.fromString(investorId), new Hbar(amount * redemptionPrice))
        .freezeWith(client);

    const signTx = await tx.sign(operatorKey);
    const txResponse = await signTx.execute(client);
    const receipt = await txResponse.getReceipt(client);
    console.log(`✅ Redeemed ${amount} bonds for ${amount * redemptionPrice} HBAR.`);
}

async function checkBalance() {
    const balance = await new AccountBalanceQuery()
        .setAccountId(process.env.OPERATOR_ID)
        .execute(client);

    console.log(`💰 Account Balance: ${balance.hbars.toString()} HBAR`);
}



/**
 * Execute the Tokenization Process
 */
async function main() {
    await createBondToken();
    await distributeBonds("0.0.5775431", 50); // Replace with actual investor ID
    await payCoupon("0.0.5775431", 10); // Pay 10 HBAR coupon
    await redeemBond("0.0.5775431", 50); // Redeem bonds at maturity
}

// main().catch(console.error);
checkBalance().catch(console.error);
