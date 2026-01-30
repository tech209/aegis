async function main() {
    const CreditSnapshotNFT = await hre.ethers.getContractFactory("CreditSnapshotNFT");
    const creditSnapshot = await CreditSnapshotNFT.deploy();

    await creditSnapshot.waitForDeployment();

    console.log("CreditSnapshotNFT deployed to:", await creditSnapshot.getAddress());
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
