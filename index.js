require("dotenv").config(); // Load environment variables from .env file
const { Hbar, Client, AccountId, PrivateKey, TokenCreateTransaction } = require("@hashgraph/sdk");

async function environmentSetup() {
  // Grab your Hedera testnet account ID and private key from the .env file
  const myAccountId = process.env.MY_ACCOUNT_ID, myPrivateKey = process.env.MY_PRIVATE_KEY;
  
  // Throw an error if environment variables are not found
  if (!myAccountId || !myPrivateKey) throw new Error("Environment variables MY_ACCOUNT_ID and MY_PRIVATE_KEY must be present");

  // Create your Hedera Testnet client and set the operator
  const client = Client.forTestnet();
  client.setOperator(AccountId.fromString(myAccountId), PrivateKey.fromStringDer(myPrivateKey))
        .setDefaultMaxTransactionFee(new Hbar(100)) // Set default max transaction fee
        .setDefaultMaxQueryPayment(new Hbar(50)); // Set max payment for queries

  // Create a new token with specified properties
  const transaction = new TokenCreateTransaction()
    .setTokenName("MyFirstCrypto") // Set token name
    .setTokenSymbol("MFC") // Set token symbol
    .setTreasuryAccountId(AccountId.fromString(myAccountId)) // Set treasury account
    .setInitialSupply(5000) // Set initial supply of the token
    .setAdminKey(PrivateKey.fromStringDer(myPrivateKey)) // Set admin key
    .freezeWith(client); // Freeze the transaction for signing

  // Sign the transaction and submit to the Hedera network
  const signedTransaction = await transaction.sign(PrivateKey.fromStringDer(myPrivateKey));
  const transactionResponse = await signedTransaction.execute(client);

  // Request and obtain the receipt of the transaction
  const receipt = await transactionResponse.getReceipt(client);

  // Get and print the new token ID from the receipt
  const tokenId = receipt.tokenId;
  console.log("The new token ID is " + tokenId);
}

// Execute the environment setup function and catch any errors
environmentSetup().catch(console.error);
