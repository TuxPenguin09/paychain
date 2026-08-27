from web3 import Web3
from config import POLYGON_AMOY_RPC_URL, PAYCHAIN_CONTRACT_ADDRESS

PAYCHAIN_ABI = [
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalDeposited",
        "outputs": [{"type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"type": "address"}, {"type": "string"}],
        "name": "registerEmployee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [{"type": "address"}, {"type": "uint256"}],
        "name": "recordSalary",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"type": "uint256"}],
        "name": "salaryRecords",
        "outputs": [
            {"type": "uint256"},
            {"type": "address"},
            {"type": "uint256"},
            {"type": "uint256"},
            {"type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "type": "address", "name": "employee"},
            {"type": "string", "name": "name"},
        ],
        "name": "EmployeeRegistered",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "type": "address", "name": "from"},
            {"type": "uint256", "name": "amount"},
            {"type": "uint256", "name": "totalBalance"},
        ],
        "name": "SalaryDeposited",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "type": "uint256", "name": "salaryId"},
            {"indexed": True, "type": "address", "name": "employee"},
            {"type": "uint256", "name": "amount"},
            {"type": "uint256", "name": "timestamp"},
        ],
        "name": "SalaryDisbursed",
        "type": "event",
    },
]


class Web3Service:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(POLYGON_AMOY_RPC_URL))
        self.connected = self.w3.is_connected()
        self.contract = None
        if PAYCHAIN_CONTRACT_ADDRESS:
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(PAYCHAIN_CONTRACT_ADDRESS),
                abi=PAYCHAIN_ABI,
            )

    def get_block_number(self) -> int:
        return self.w3.eth.block_number

    def get_balance(self, address: str) -> int:
        return self.w3.eth.get_balance(Web3.to_checksum_address(address))

    def get_contract_owner(self) -> str | None:
        if not self.contract:
            return None
        return self.contract.functions.owner().call()

    def get_total_deposited(self) -> int:
        if not self.contract:
            return 0
        return self.contract.functions.totalDeposited().call()

    def get_salary_record(self, salary_id: int) -> dict | None:
        if not self.contract:
            return None
        record = self.contract.functions.salaryRecords(salary_id).call()
        return {
            "id": record[0],
            "employee": record[1],
            "amount": record[2],
            "timestamp": record[3],
            "disbursed": record[4],
        }

    def get_employee_balance(self, employee_address: str) -> int:
        if not self.contract:
            return 0
        return self.contract.functions.employeeBalances(
            Web3.to_checksum_address(employee_address)
        ).call()


web3_service = Web3Service()
