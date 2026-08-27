import { expect } from "chai";
import hre from "hardhat";

describe("PayChain", function () {
  async function deployFixture() {
    const { ethers, networkHelpers } = await hre.network.create();
    const [owner, alice, bob] = await ethers.getSigners();

    const paychain = await ethers.deployContract("PayChain");
    await paychain.waitForDeployment();

    return { paychain, owner, alice, bob, ethers, networkHelpers };
  }

  describe("Deployment", function () {
    it("should set the deployer as owner", async function () {
      const { paychain, owner } = await deployFixture();
      expect(await paychain.owner()).to.equal(owner.address);
    });

    it("should start with zero total deposited", async function () {
      const { paychain } = await deployFixture();
      expect(await paychain.totalDeposited()).to.equal(0n);
    });
  });

  describe("Employee Registration", function () {
    it("should emit EmployeeRegistered event", async function () {
      const { paychain, alice } = await deployFixture();
      await expect(paychain.registerEmployee(alice.address, "Maria Santos"))
        .to.emit(paychain, "EmployeeRegistered")
        .withArgs(alice.address, "Maria Santos");
    });

    it("should revert when non-owner tries to register", async function () {
      const { paychain, alice } = await deployFixture();
      await expect(
        paychain.connect(alice).registerEmployee(alice.address, "Maria Santos")
      ).to.be.revertedWith("PayChain: caller is not the owner");
    });

    it("should revert when registering zero address", async function () {
      const { paychain } = await deployFixture();
      await expect(
        paychain.registerEmployee(hre.ethers.ZeroAddress, "Nobody")
      ).to.be.revertedWith("PayChain: zero address");
    });
  });

  describe("Deposits", function () {
    it("should accept MATIC deposits", async function () {
      const { paychain, owner } = await deployFixture();
      await paychain.deposit({ value: hre.ethers.parseEther("1.0") });
      expect(await paychain.totalDeposited()).to.equal(hre.ethers.parseEther("1.0"));
    });

    it("should emit SalaryDeposited event", async function () {
      const { paychain } = await deployFixture();
      const amount = hre.ethers.parseEther("2.0");
      await expect(paychain.deposit({ value: amount }))
        .to.emit(paychain, "SalaryDeposited")
        .withArgs((await hre.ethers.getSigners())[0].address, amount, amount);
    });

    it("should revert on zero deposit", async function () {
      const { paychain } = await deployFixture();
      await expect(paychain.deposit({ value: 0 })).to.be.revertedWith(
        "PayChain: zero deposit"
      );
    });
  });

  describe("Salary Recording", function () {
    it("should record and emit salary disbursement", async function () {
      const { paychain, alice } = await deployFixture();
      const amount = hre.ethers.parseEther("0.5");
      await paychain.deposit({ value: hre.ethers.parseEther("5.0") });

      const tx = paychain.recordSalary(alice.address, amount);
      await expect(tx).to.emit(paychain, "SalaryDisbursed");

      const record = await paychain.salaryRecords(0);
      expect(record.employee).to.equal(alice.address);
      expect(record.amount).to.equal(amount);
    });

    it("should deduct from total deposited", async function () {
      const { paychain, alice } = await deployFixture();
      await paychain.deposit({ value: hre.ethers.parseEther("5.0") });
      await paychain.recordSalary(alice.address, hre.ethers.parseEther("2.0"));

      expect(await paychain.totalDeposited()).to.equal(hre.ethers.parseEther("3.0"));
    });

    it("should revert when insufficient balance", async function () {
      const { paychain, alice } = await deployFixture();
      await paychain.deposit({ value: hre.ethers.parseEther("1.0") });
      await expect(
        paychain.recordSalary(alice.address, hre.ethers.parseEther("2.0"))
      ).to.be.revertedWith("PayChain: insufficient balance");
    });
  });

  describe("Ownership Transfer", function () {
    it("should transfer ownership", async function () {
      const { paychain, alice } = await deployFixture();
      await paychain.transferOwner(alice.address);
      expect(await paychain.owner()).to.equal(alice.address);
    });

    it("should emit OwnerTransferred event", async function () {
      const { paychain, owner, alice } = await deployFixture();
      await expect(paychain.transferOwner(alice.address))
        .to.emit(paychain, "OwnerTransferred")
        .withArgs(owner.address, alice.address);
    });

    it("should revert when non-owner tries to transfer", async function () {
      const { paychain, alice } = await deployFixture();
      await expect(
        paychain.connect(alice).transferOwner(alice.address)
      ).to.be.revertedWith("PayChain: caller is not the owner");
    });
  });

  describe("Receive", function () {
    it("should accept direct MATIC transfers", async function () {
      const { paychain, owner } = await deployFixture();
      await owner.sendTransaction({
        to: await paychain.getAddress(),
        value: hre.ethers.parseEther("3.0"),
      });
      expect(await paychain.totalDeposited()).to.equal(hre.ethers.parseEther("3.0"));
    });
  });
});
