# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aegis is a blockchain-based PoC that creates provable, timestamped credit score snapshots as ERC-721 NFTs. Users mint an NFT containing their credit score and the block timestamp, giving them an immutable on-chain proof of their creditworthiness at a specific moment.

## Development Commands

### Starting the Development Environment

All commands run from the `aegis/` subdirectory.

```bash
# Terminal 1: Start Hardhat local testnet
npx hardhat node

# Terminal 2: Deploy smart contract (after testnet is running)
npx hardhat run scripts/deploy.js --network localhost

# Terminal 3: Start Flask server
python run.py
```

The application runs at http://127.0.0.1:5000

### Hardhat Commands

```bash
npx hardhat compile          # Compile Solidity contracts
npx hardhat test             # Run contract tests
npx hardhat node             # Start local testnet (port 8545)
```

### Dependencies

```bash
pip install -r aegis/requirements.txt
npm install                                # from aegis/ directory
```

## Architecture

```
Frontend (Jinja2/JS) → Flask Backend → Web3.py → CreditSnapshotNFT.sol (ERC-721) → Hardhat Testnet
```

### Key Directories

- **`aegis/app/`** - Flask application (routes, models, credit API interface)
- **`aegis/contracts/`** - Solidity smart contracts
- **`aegis/templates/`** - Jinja2 HTML templates
- **`aegis/static/`** - CSS and JavaScript assets
- **`aegis/scripts/`** - Hardhat deployment scripts

### Core Files

| File | Purpose |
|------|---------|
| `aegis/app/routes.py` | Flask HTTP endpoints (mint and query snapshots) |
| `aegis/app/models.py` | Web3.py contract interaction layer |
| `aegis/app/credit_api.py` | Credit provider interface (manual entry now, API-ready) |
| `aegis/contracts/CreditSnapshotNFT.sol` | ERC-721 NFT contract for credit snapshots |
| `aegis/scripts/deploy.js` | Contract deployment script |
| `aegis/run.py` | Application entry point |

### Data Flow

1. User submits wallet address + credit score via `/upload` form
2. `routes.py` validates input and calls `models.mint_snapshot()`
3. Contract mints an ERC-721 NFT with the score and block.timestamp
4. User receives token ID and transaction hash
5. Verification via `/verify` queries by wallet address or token ID

### Smart Contract Interface (CreditSnapshotNFT.sol)

ERC-721 (with Enumerable) contract:
- `mint(address to, uint256 creditScore)` - Mint snapshot NFT (score must be 300-850)
- `getSnapshot(uint256 tokenId)` - Returns (creditScore, timestamp, owner)
- `getSnapshotsByOwner(address owner)` - Returns all snapshots for a wallet
- `getTokensByOwner(address owner)` - Returns token IDs for a wallet

### Credit API Module (credit_api.py)

Abstract `CreditProvider` interface for future credit bureau API integration:
- `ManualEntryProvider` - Current PoC (user enters score manually)
- `MockAPIProvider` - For testing
- Placeholder for Experian/Equifax/TransUnion providers

## Technology Stack

- **Backend**: Python 3, Flask 3.0.0, Web3.py
- **Blockchain**: Hardhat 2.22.18, Solidity 0.8.28, OpenZeppelin Contracts (ERC-721)
- **Frontend**: Jinja2, vanilla JavaScript

## Important Notes

- Contract address is hardcoded in `models.py` - update after redeployment
- This is a PoC with hardcoded config - not production-ready
- Hardhat testnet uses chain ID 31337 and listens on port 8545
- The old fingerprint/biometric identity system (`identity.py`) has been deprecated in favor of wallet-based identity via NFT ownership
