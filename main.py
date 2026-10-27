import json


class Cliente:

    def __init__(self, id: int, nome: str, email: str, fone: str):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__fone = fone

    def get_id(self) -> int:
        return self.__id

    def set_id(self, id: int):
        self.__id = id

    def get_nome(self) -> str:
        return self.__nome

    def set_nome(self, nome: str):
        self.__nome = nome

    def get_email(self) -> str:
        return self.__email

    def set_email(self, email: str):
        self.__email = email

    def get_fone(self) -> str:
        return self.__fone

    def set_fone(self, fone: str):
        self.__fone = fone

    def ToString(self) -> str:
        return f"ID: {self.__id} | Nome: {self.__nome} | Email: {self.__email} | Fone: {self.__fone}"

    def __str__(self) -> str:
        return self.ToString()

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "nome": self.__nome,
            "email": self.__email,
            "fone": self.__fone,
        }

    @staticmethod
    def from_dict(d: dict):
        return Cliente(d["id"], d["nome"], d["email"], d["fone"])


class ClienteDAO:
    objetos = []

    @classmethod
    def Inserir(cls, obj: Cliente) -> None:
        cls.Abrir()
        cls.objetos.append(obj)
        cls.Salvar()

    @classmethod
    def Listar(cls) -> list:
        cls.Abrir()
        return cls.objetos

    @classmethod
    def Listar_Id(cls, id: int) -> Cliente:
        cls.Abrir()
        for c in cls.objetos:
            if c.get_id() == id:
                return c
        return None

    @classmethod
    def Atualizar(cls, obj: Cliente) -> None:
        cls.Abrir()
        c = cls.Listar_Id(obj.get_id())
        if c is not None:
            c.set_nome(obj.get_nome())
            c.set_email(obj.get_email())
            c.set_fone(obj.get_fone())
            cls.Salvar()

    @classmethod
    def Excluir(cls, obj: Cliente) -> None:
        cls.Abrir()
        c = cls.Listar_Id(obj.get_id())
        if c is not None:
            cls.objetos.remove(c)
            cls.Salvar()

    @classmethod
    def Abrir(cls) -> None:
        try:
            with open("clientes.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                cls.objetos = [Cliente.from_dict(d) for d in dados]
        except (FileNotFoundError, json.JSONDecodeError):
            cls.objetos = []

    @classmethod
    def Salvar(cls) -> None:
        with open("clientes.json", "w", encoding="utf-8") as f:
            dados = [c.to_dict() for c in cls.objetos]
            json.dump(dados, f, ensure_ascii=False, indent=4)


class UI:

    @staticmethod
    def Menu() -> int:
        print("\n--- MENU CLIENTES ---")
        print("1 - Listar clientes")
        print("2 - Inserir cliente")
        print("3 - Atualizar cliente")
        print("4 - Excluir cliente")
        print("0 - Sair")
        try:
            op = int(input("Informe a opção: "))
            return op
        except ValueError:
            return -1

    @staticmethod
    def Cliente_Listar() -> None:
        clientes = ClienteDAO.Listar()
        if len(clientes) == 0:
            print("Nenhum cliente cadastrado.")
        else:
            for c in clientes:
                print(c.ToString())

    @staticmethod
    def Cliente_Inserir() -> None:
        try:
            id = int(input("ID: "))
            if ClienteDAO.Listar_Id(id) is not None:
                print("Erro: Já existe um cliente com este ID.")
                return
            nome = input("Nome: ")
            email = input("Email: ")
            fone = input("Fone: ")
            c = Cliente(id, nome, email, fone)
            ClienteDAO.Inserir(c)
            print("Cliente inserido com sucesso!")
        except ValueError:
            print("Entrada inválida.")

    @staticmethod
    def Cliente_Atualizar() -> None:
        try:
            id = int(input("ID do cliente a ser atualizado: "))
            c = ClienteDAO.Listar_Id(id)
            if c is None:
                print("Cliente não encontrado.")
            else:
                nome = input("Novo Nome: ")
                email = input("Novo Email: ")
                fone = input("Novo Fone: ")
                c_novo = Cliente(id, nome, email, fone)
                ClienteDAO.Atualizar(c_novo)
                print("Cliente atualizado com sucesso!")
        except ValueError:
            print("Entrada inválida.")

    @staticmethod
    def Cliente_Excluir() -> None:
        try:
            id = int(input("ID do cliente a ser excluído: "))
            c = ClienteDAO.Listar_Id(id)
            if c is None:
                print("Cliente não encontrado.")
            else:
                ClienteDAO.Excluir(c)
                print("Cliente excluído com sucesso!")
        except ValueError:
            print("Entrada inválida.")

    @staticmethod
    def Main() -> None:
        op = -1
        while op != 0:
            op = UI.Menu()
            if op == 1:
                UI.Cliente_Listar()
            elif op == 2:
                UI.Cliente_Inserir()
            elif op == 3:
                UI.Cliente_Atualizar()
            elif op == 4:
                UI.Cliente_Excluir()
            elif op == 0:
                print("Programa finalizado.")
            else:
                print("Opção inválida!")


if __name__ == "__main__":
    UI.Main()