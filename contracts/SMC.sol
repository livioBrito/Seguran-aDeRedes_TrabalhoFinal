pragma solidity >=0.4.25 <0.6.0;

contract SMC {
    enum StatesSMC { State1, Punishment }

    bool[4][6] public truthTable;
    bool[4][6] public truthTableA;
    bool[4][6] public truthTableB;
    uint public la1;
    uint public la2;
    uint public lb1;
    uint public lb2;
    bool public invA;
    bool public invB;
    uint public punishmentAmount;
    address payable public accountA;
    address payable public accountB;

    StatesSMC public myState;

    constructor(bool[24] memory _tt, bool[24] memory _tta, address payable _accountA, address payable _accountB) public {
        for (uint i = 0; i < 4; i++) {
            for (uint j = 0; j < 6; j++) {
                truthTable[i][j] = _tt[i * 6 + j];
                truthTableA[i][j] = _tta[i * 6 + j];
            }
        }
        accountA = _accountA;
        accountB = _accountB;
    }

    function receiveTableFromB(bool[4][6] memory _tt) public {
        for (uint i = 0; i < 4; i++) {
            for (uint j = 0; j < 6; j++) {
                truthTableB[i][j] = _tt[i][j];
            }
        }
    }

    function receiveLinesFromA(uint _l1, uint _l2) public {
        la1 = _l1;
        la2 = _l2;
    }

    function receiveLinesFromB(uint _l1, uint _l2) public {
        lb1 = _l1;
        lb2 = _l2;
    }

    function receiveInversionFromA(bool _inv) public {
        invA = _inv;
    }

    function receiveInversionFromB(bool _inv) public {
        invB = _inv;
    }

    function getLine() public view returns (uint) {
        uint linha;
        if ((la1 == lb1) || (la1 == lb2)) {
            linha = la1;
        }
        if ((la2 == lb1) || (la2 == lb2)) {
            linha = la2;
        }
        return linha;
    }

    function getValue() public view returns (bool) {
        uint linha;
        bool r;
        if ((la1 == lb1) || (la1 == lb2)) {
            linha = la1;
        }
        if ((la2 == lb1) || (la2 == lb2)) {
            linha = la2;
        }
        r = truthTableB[linha][3];
        return (r != invA) != invB;
    }

    event PunishmentApplied(address indexed punished, uint amount);

    function applyPunishment() public {
        require(myState == StatesSMC.Punishment, "Not in punishment state");
        
        // Neste exemplo, transferimos Ether como punição
        bool punishAccountA = true;

        if (punishAccountA) {
            uint balance = address(this).balance;
            punishmentAmount = balance; // Aqui, estou usando todo o saldo do contrato como punição, você pode definir um valor específico
            accountB.transfer(punishmentAmount);
                        emit PunishmentApplied(accountA, punishmentAmount);
        } else {
            // Punir a conta B, se necessário
            uint balance = address(this).balance;
            punishmentAmount = balance; // Aqui, estou usando todo o saldo do contrato como punição, você pode definir um valor específico
            accountA.transfer(punishmentAmount);
            emit PunishmentApplied(accountB, punishmentAmount);
        }
    }

    function checkForPunishment() public {
        // Por exemplo, se os resultados não são iguais ou outras condições específicas do seu caso de uso
        bool punishmentNeeded = getValue() != truthTableB[getLine()][3];

        if (punishmentNeeded) {
            myState = StatesSMC.Punishment;
            applyPunishment();
        }
    }

    // Função fallback para receber Ether
    function() external payable {}

    function validateTable(bool[4][6] memory table) private pure returns (bool) {
        bool valid = true;
        // verifica se a tabela tem o tamanho correto
        if (table.length != 4 || table[0].length != 6) {
            valid = false;
        }
        // verifica se os valores são válidos (apenas 0 ou 1)
        for (uint i = 0; i < table.length; i++) {
            for (uint j = 0; j < table[i].length; j++) {
                if (table[i][j] != false && table[i][j] != true) {
                    valid = false;
                }
            }
        }
        // retorna se a tabela é válida ou não
        return valid;
    }
}
