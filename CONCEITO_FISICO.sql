CREATE DATABASE MERCADO;

USE MERCADO;

CREATE TABLE CLIENTE(
	CPF VARCHAR(15) PRIMARY KEY,
	NOME VARCHAR(50) NOT NULL,
	SOBRENOME VARCHAR(50) NOT NULL,
	EMAIL VARCHAR(30) NOT NULL UNIQUE,
	SEXO ENUM('M', 'F') NOT NULL,
	NASCIMENTO DATE NOT NULL
);


CREATE TABLE ENDERECO(
	IDENDERECO INT PRIMARY KEY AUTO_INCREMENT,
	RUA VARCHAR(50) NOT NULL,
	BAIRRO VARCHAR(50) NOT NULL,
	CIDADE VARCHAR(50) NOT NULL,
	NUMERO VARCHAR(5) NOT NULL,
	CEP VARCHAR(12) NOT NULL,
	CPF_CLIENTE VARCHAR(15)
);


CREATE TABLE VENDA(
	IDVENDA INT PRIMARY KEY AUTO_INCREMENT,
	VALOR_TOTAL FLOAT(10,2) NOT NULL,
	DATA DATETIME NOT NULL,
	ECONOMIA_CLIENTE FLOAT(10,2),
	CPF_CLIENTE VARCHAR(15)
);


CREATE TABLE OPCAO(
	IDOPCAO INT PRIMARY KEY AUTO_INCREMENT,
	VALOR_PAGO FLOAT NOT NULL,
	TIPO VARCHAR(30) NOT NULL,
	ID_VENDA INT
);


CREATE TABLE PRODUTO(
	CODIGO INT PRIMARY KEY,
	PRECO_NORMAL FLOAT(10,2) NOT NULL,
	PRECO_CLIENTE FLOAT(10,2),
	DESCRICAO VARCHAR(50) NOT NULL
);



ALTER TABLE OPCAO ADD CONSTRAINT FK_VENDA_OPCAO
FOREIGN KEY (ID_VENDA) REFERENCES VENDA(IDVENDA);

ALTER TABLE ENDERECO 
ADD CONSTRAINT FK_CLIENTE_ENDERECO
FOREIGN KEY (CPF_CLIENTE) REFERENCES CLIENTE(CPF);

ALTER TABLE VENDA 
ADD CONSTRAINT FK_CLIENTE_VENDA
FOREIGN KEY (CPF_CLIENTE) REFERENCES CLIENTE(CPF);



INSERT INTO PRODUTO VALUES('2295', 5.99, 4.99, 'Banana Nanica kg');
INSERT INTO PRODUTO VALUES('2219', 7.99, NULL, 'Banana prata kg');
INSERT INTO PRODUTO VALUES('2172', 9.99, NULL, 'Maçã Fuji kg');
INSERT INTO PRODUTO VALUES('2547', 8.99, NULL, 'Maçã Gala kg');
INSERT INTO PRODUTO VALUES('2127', 12.40, 8.69, 'Mamão Papaya kg');
INSERT INTO PRODUTO VALUES('2134', 10.99, NULL, 'Mamão Formosa kg');
INSERT INTO PRODUTO VALUES('5843', 12.00, NULL, 'Pão Francês kg');
INSERT INTO PRODUTO VALUES('1052', 8.99, 5.99, 'Tomate Carmem kg');
INSERT INTO PRODUTO VALUES('7622210194046', 12.27, 11.99, 'CHOCOLATE MILKA 100G un');
INSERT INTO PRODUTO VALUES('9788575225639', 56.00, NULL, 'Entendendo algoritmos un');
INSERT INTO PRODUTO VALUES('5601229873236', 3.00, NULL, 'Lapiseira Molin 0,7mm un');
INSERT INTO PRODUTO VALUES('7898938236034', 6.69, 4.99, 'Coca-Cola Garrafa Pet 2L un');

-- ALGUNS POSSÍVEIS RELATÓRIOS PARA NEGÓCIOS
CREATE VIEW RELATORIO_CLIENTE AS
	SELECT C.CPF, C.NOME, C.SOBRENOME, E.CIDADE, E.CEP, SUM(V.VALOR_TOTAL) AS TOTAL_GASTO, SUM(V.ECONOMIA_CLIENTE) AS ECONOMIA_TOTAL FROM CLIENTE C
	LEFT JOIN ENDERECO E
	ON C.CPF = E.CPF_CLIENTE
	LEFT JOIN VENDA V
	ON C.CPF = V.CPF_CLIENTE
	GROUP BY 1
	ORDER BY 6 DESC;
	
	
CREATE VIEW RELATORIO_CIDADE AS
	SELECT E.CIDADE, SUM(V.VALOR_TOTAL) AS TOTAL_GASTO FROM ENDERECO E
	LEFT JOIN VENDA V
	ON E.CPF_CLIENTE = V.CPF_CLIENTE
	GROUP BY 1
	ORDER BY 2 DESC;


-- CRIAÇÃO DE TRIGGER QUE IDENTIFICA ALTERAÇÕES NO PRECO E ARMAZENA EM UMA TABELA.
CREATE TABLE MUDANCA_PRECO(
	IDBACKUP INT PRIMARY KEY AUTO_INCREMENT,
	CODIGO VARCHAR(30) NOT NULL,
	PRECO FLOAT(10,2) NOT NULL,
	PRECO_NOVO FLOAT(10,2) NOT NULL,
	DATA DATETIME NOT NULL,
	USUARIO VARCHAR(100) NOT NULL,
	ACAO VARCHAR(200)
);


DELIMITER #
CREATE TRIGGER UPDATE_PRECO
AFTER UPDATE ON PRODUTO
FOR EACH ROW
BEGIN
	DECLARE P_ACAO VARCHAR(200) DEFAULT NULL;
	
	IF OLD.PRECO_CLIENTE != NEW.PRECO_CLIENTE THEN
		SET P_ACAO = "ALTERAÇÃO PRECO DO CLIENTE";
		INSERT INTO MUDANCA_PRECO(IDBACKUP, CODIGO, PRECO, PRECO_NOVO, DATA, USUARIO, ACAO)
	    VALUES(NULL,
			   NEW.CODIGO,
			   OLD.PRECO_CLIENTE,
			   NEW.PRECO_CLIENTE,
			   NOW(),
			   USER(),
			   P_ACAO);
	END IF;
	IF OLD.PRECO_NORMAL != NEW.PRECO_NORMAL THEN
		SET P_ACAO = "ALTERAÇÃO PRECO NORMAL";
		INSERT INTO MUDANCA_PRECO(IDBACKUP, CODIGO, PRECO, PRECO_NOVO, DATA, USUARIO, ACAO)
	    VALUES(NULL,
			   NEW.CODIGO,
			   OLD.PRECO_NORMAL,
			   NEW.PRECO_NORMAL,
			   NOW(),
			   USER(),
			   P_ACAO);
	END IF;
END #
delimiter ;
