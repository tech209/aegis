# Aegis Blockchain PoC 🛡️

### Overview
Aegis is a blockchain-based system that securely stores credit snapshots using a decentralized ledger.

### Features
✅ Stores credit snapshots on a Hardhat-based Ethereum blockchain  
✅ Uses **hashed fingerprints (`user_id`)** for identity verification  
✅ Prevents duplicate submissions & redirects users to verification  
✅ Allows **querying stored snapshots by fingerprint**

### Setup & Deployment
1. **Clone the repo**  
   ```bash
   git clone https://github.com/tech209/aegis.git
   cd aegis
   ```
2. **Start Hardhat testnet**
    ```bash
    npx hardhat node
    ```
3. **Deploy smart contract**
    ```bash
    npx hardhat run scripts/deploy.js --network localhost
    ```
4. **Deploy smart contract**
    ```bash
    python run.py
    ```
5. **Submit a credit snapshot at**
    ```bash
    👉 http://127.0.0.1:5000/upload
    ```
6. **Verify stored data using Hardhat console**
```js
await AegisCredit.getCreditSnapshotByFingerprint("your_fingerprint_here");
```
# **Next Steps**
Move to a public testnet (Goerli, Sepolia, Polygon Mumbai)
Integrate Web3 wallet support (MetaMask)
Improve frontend UI/UX

# **License**
GPL3