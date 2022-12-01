class Team: 

    def __init__(self, name, flag, fifa_code, group, id):
        self.name = name
        self.flag = flag
        self.fifa_code = fifa_code
        self.group = group
        self.id = int(id) 
        pass

    def get_name(self): 
        return self.name

    def print_team(self): 
        print("""
            -----País: {}
            -----URL Flag: {}
            -----Código FIFA: {}
            -----Grupo: {}
            -----ID: {}
            """.format(self.name, self.flag, self.fifa_code, self.group, self.id))


    