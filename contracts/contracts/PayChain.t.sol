// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

import "forge-std/Test.sol";
import "../PayChain.sol";

contract PayChainTest is Test {
    PayChain public paychain;
    address public owner = address(this);
    address public alice = makeAddr("alice");
    address public bob = makeAddr("bob");

    function setUp() public {
        paychain = new PayChain();
    }

    function test_InitialOwner() public view {
        assertEq(paychain.owner(), owner);
    }

    function test_InitialBalance() public view {
        assertEq(paychain.totalDeposited(), 0);
    }

    function test_RegisterEmployee() public {
        paychain.registerEmployee(alice, "Maria Santos");
    }

    function test_Deposit() public payable {
        vm.deal(owner, 1 ether);
        paychain.deposit{value: 1 ether}();
        assertEq(paychain.totalDeposited(), 1 ether);
    }

    function test_RecordSalary() public {
        vm.deal(owner, 5 ether);
        paychain.deposit{value: 5 ether}();

        paychain.recordSalary(alice, 1 ether);
        assertEq(paychain.totalDeposited(), 4 ether);

        (, address employee, uint256 amount,,) = paychain.salaryRecords(0);
        assertEq(employee, alice);
        assertEq(amount, 1 ether);
    }

    function test_RecordSalaryMultipleEmployees() public {
        vm.deal(owner, 10 ether);
        paychain.deposit{value: 10 ether}();

        paychain.recordSalary(alice, 3 ether);
        paychain.recordSalary(bob, 2 ether);

        assertEq(paychain.totalDeposited(), 5 ether);

        (,, uint256 amountAlice,,) = paychain.salaryRecords(0);
        assertEq(amountAlice, 3 ether);

        (,, uint256 amountBob,,) = paychain.salaryRecords(1);
        assertEq(amountBob, 2 ether);
    }

    function test_RevertRecordSalaryInsufficientBalance() public {
        vm.deal(owner, 1 ether);
        paychain.deposit{value: 1 ether}();

        vm.expectRevert("PayChain: insufficient balance");
        paychain.recordSalary(alice, 2 ether);
    }

    function test_RevertRecordSalaryZeroAmount() public {
        vm.expectRevert("PayChain: zero amount");
        paychain.recordSalary(alice, 0);
    }

    function test_RevertRecordSalaryZeroAddress() public {
        vm.expectRevert("PayChain: zero address");
        paychain.recordSalary(address(0), 1 ether);
    }

    function test_RevertOnlyOwner() public {
        vm.prank(alice);
        vm.expectRevert("PayChain: caller is not the owner");
        paychain.registerEmployee(bob, "Juan Dela Cruz");
    }

    function test_TransferOwner() public {
        paychain.transferOwner(alice);
        assertEq(paychain.owner(), alice);
    }

    function test_RevertTransferOwnerZeroAddress() public {
        vm.expectRevert("PayChain: zero address");
        paychain.transferOwner(address(0));
    }

    function test_Receive() public payable {
        vm.deal(owner, 2 ether);
        (bool sent,) = address(paychain).call{value: 2 ether}("");
        require(sent, "Failed to send Ether");
        assertEq(paychain.totalDeposited(), 2 ether);
    }

    function testFuzz_Deposit(uint8 amount) public {
        vm.assume(amount > 0);
        vm.deal(owner, amount);
        paychain.deposit{value: amount}();
        assertEq(paychain.totalDeposited(), amount);
    }
}
