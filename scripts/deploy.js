async function main() {
    const AegisCredit = await hre.ethers.getContractFactory("AegisCredit"); // Use 'hre.ethers' properly
    const aegisCredit = await AegisCredit.deploy();  // Deploy the contract

    await aegisCredit.waitForDeployment();  // Ensure it's deployed before logging

    console.log("AegisCredit deployed to:", await aegisCredit.getAddress()); // Get the deployed contract address
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
