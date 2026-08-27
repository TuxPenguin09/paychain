// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract PayChain {
    address public owner;
    uint256 public totalDeposited;
    uint256 public nonce;

    struct SalaryRecord {
        uint256 id;
        address employee;
        uint256 amount;
        uint256 timestamp;
        bool disbursed;
    }

    mapping(address => uint256) public employeeBalances;
    mapping(uint256 => SalaryRecord) public salaryRecords;
    mapping(uint256 => bool) public salaryClaimed;
    uint256 public nextSalaryId;

    event EmployeeRegistered(address indexed employee, string name);
    event SalaryDeposited(address indexed from, uint256 amount, uint256 totalBalance);
    event SalaryDisbursed(uint256 indexed salaryId, address indexed employee, uint256 amount, uint256 timestamp);
    event OwnerTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "PayChain: caller is not the owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerEmployee(address employee, string calldata employeeName) external onlyOwner {
        require(employee != address(0), "PayChain: zero address");
        emit EmployeeRegistered(employee, employeeName);
    }

    function deposit() external payable onlyOwner {
        require(msg.value > 0, "PayChain: zero deposit");
        totalDeposited += msg.value;
        emit SalaryDeposited(msg.sender, msg.value, totalDeposited);
    }

    function recordSalary(address employee, uint256 amount) external onlyOwner {
        require(employee != address(0), "PayChain: zero address");
        require(amount > 0, "PayChain: zero amount");
        require(totalDeposited >= amount, "PayChain: insufficient balance");

        totalDeposited -= amount;

        uint256 salaryId = nextSalaryId++;
        salaryRecords[salaryId] = SalaryRecord({
            id: salaryId,
            employee: employee,
            amount: amount,
            timestamp: block.timestamp,
            disbursed: false
        });

        emit SalaryDisbursed(salaryId, employee, amount, block.timestamp);
    }

    function transferOwner(address newOwner) external onlyOwner {
        require(newOwner != address(0), "PayChain: zero address");
        emit OwnerTransferred(owner, newOwner);
        owner = newOwner;
    }

    receive() external payable {
        totalDeposited += msg.value;
    }
}
