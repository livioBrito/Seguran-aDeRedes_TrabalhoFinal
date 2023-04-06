# *Smart Contracts* como uma plataforma para computação segura (SBSeg 2020)

Esse repositório provê a implementação da prova de conceito do artigo "*Smart Contracts* como uma plataforma para computação segura", o qual foi escrito por Ivan da Silva Sendin (@ivansendin) e Bianca Cristina da Silva (@BiancaCritina) e submetido ao Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais (SBSeg) 2020. 

## Visão geral
A prova de conceito consiste na implementação de um *smart contract* que permite a execução de computações de tabelas-verdade entre múltiplas entidades. Para tal, a ferramenta Brownie (documentação disponível [aqui](https://eth-brownie.readthedocs.io/en/stable/)), framework que permite o desenvolvimento e teste de *smart contracts* por meio da simulação da *Ethereum Virtual Machine (EVM)*. 

Dessa forma, o projeto segue as diretrizes da estrutura proposta pelo Brownie. Assim,

* /projects: contratos desenvolvidos
* /interfaces: interfaces desenvolvidas
* /scripts: scripts desenvolvidos para interação com os contratos
* /tests: scripts para testes do projeto
* /build: dados do projetos
* /reports: relatórios JSON

## Instalação
### Pré requisitos
É necessário instalar o Brownie e Ganache para, futuramente, conseguir executar o projeto. Siga [esse tutorial](https://medium.com/better-programming/part-1-brownie-smart-contracts-framework-for-ethereum-basics-5efc80205413) para instalar tais ferramentas. 

### Projeto
Para instalar o projeto localmente basta realizar o clone do repositório.

**Via HTTP**:
```
git clone https://github.com/BiancaCristina/Artigo-SC.git
```

**Via SSH**:
```
git clone git@github.com:BiancaCristina/Artigo-SC.git
```

## Execução 
Para uma execução com sucesso, é necessário:
* Concluído a instalação do Brownie e Ganache
* Ter uma instância local do Ganache rodando
* Ter definido uma network (aqui denominada privada, mas o nome é livre) no Brownie.

Atendida as condições acima, basta executar os seguintes comandos para abrir o terminal do Brownie:
```
brownie compile
brownie console --network private
```

Feito isso, para executar o contrato, basta:
```python
run('execution')
```


