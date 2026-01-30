// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

contract CreditSnapshotNFT is ERC721, ERC721Enumerable {
    struct CreditSnapshot {
        uint256 creditScore;
        uint256 timestamp;
    }

    uint256 private _nextTokenId;

    // Token ID => Snapshot data
    mapping(uint256 => CreditSnapshot) public snapshots;

    event SnapshotMinted(
        address indexed owner,
        uint256 indexed tokenId,
        uint256 creditScore,
        uint256 timestamp
    );

    constructor() ERC721("Aegis Credit Snapshot", "AEGIS") {}

    /**
     * @dev Mint a new credit snapshot NFT
     * @param to Address to mint the NFT to
     * @param creditScore The credit score to record
     * @return tokenId The ID of the newly minted token
     */
    function mint(address to, uint256 creditScore) external returns (uint256) {
        require(creditScore >= 300 && creditScore <= 850, "Invalid credit score range");

        uint256 tokenId = _nextTokenId++;

        snapshots[tokenId] = CreditSnapshot({
            creditScore: creditScore,
            timestamp: block.timestamp
        });

        _safeMint(to, tokenId);

        emit SnapshotMinted(to, tokenId, creditScore, block.timestamp);

        return tokenId;
    }

    /**
     * @dev Get snapshot data for a token
     * @param tokenId The token ID to query
     * @return creditScore The recorded credit score
     * @return timestamp When the snapshot was created
     * @return owner Current owner of the token
     */
    function getSnapshot(uint256 tokenId) external view returns (
        uint256 creditScore,
        uint256 timestamp,
        address owner
    ) {
        require(tokenId < _nextTokenId, "Token does not exist");

        CreditSnapshot memory snapshot = snapshots[tokenId];
        return (snapshot.creditScore, snapshot.timestamp, ownerOf(tokenId));
    }

    /**
     * @dev Get all token IDs owned by an address
     * @param owner Address to query
     * @return tokenIds Array of token IDs owned by the address
     */
    function getTokensByOwner(address owner) external view returns (uint256[] memory) {
        uint256 balance = balanceOf(owner);
        uint256[] memory tokenIds = new uint256[](balance);

        for (uint256 i = 0; i < balance; i++) {
            tokenIds[i] = tokenOfOwnerByIndex(owner, i);
        }

        return tokenIds;
    }

    /**
     * @dev Get all snapshots for an owner
     * @param owner Address to query
     * @return tokenIds Array of token IDs
     * @return creditScores Array of credit scores
     * @return timestamps Array of timestamps
     */
    function getSnapshotsByOwner(address owner) external view returns (
        uint256[] memory tokenIds,
        uint256[] memory creditScores,
        uint256[] memory timestamps
    ) {
        uint256 balance = balanceOf(owner);
        tokenIds = new uint256[](balance);
        creditScores = new uint256[](balance);
        timestamps = new uint256[](balance);

        for (uint256 i = 0; i < balance; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(owner, i);
            tokenIds[i] = tokenId;
            creditScores[i] = snapshots[tokenId].creditScore;
            timestamps[i] = snapshots[tokenId].timestamp;
        }

        return (tokenIds, creditScores, timestamps);
    }

    /**
     * @dev Get the total number of snapshots minted
     */
    function totalSnapshots() external view returns (uint256) {
        return _nextTokenId;
    }

    // Required overrides for ERC721Enumerable
    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
