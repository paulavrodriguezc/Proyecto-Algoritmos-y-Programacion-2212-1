from team import Team
from stadium import Stadium

class Match():

    def __init__(self, local, visitante, date, estadio, id_partido, vendidos, asistencia, taken_seats):
        self.local = local
        self.visitante = visitante
        self.date = date
        self.estadio = estadio
        self.id_partido = int(id_partido)
        self.vendidos = vendidos
        self.asistentes = asistencia
        self.taken_seats = taken_seats
        pass

    def print_match(self): 
        """Imprime el partido, pero antes, debe buscar el nombre del estadio y el nombre de los equipos, porque los tenemos como Objetos Stadium o Team
        """        
        estadio_str = Stadium.get_name(self.estadio)
        local_str = Team.get_name(self.local)
        visitante_str = Team.get_name(self.visitante)

        print("""
        Partido #{}
        Local: {}
        Visitante: {}
        Fecha y Hora: {}
        Estadio: {}
        """.format(self.id_partido, local_str, visitante_str, self.date, estadio_str)) 

    def get_countries(self): 
        """Devuelve un string con los equipos que juegan el partido. Ideal para el módulo de busqueda. 

        Returns:
            string: nombres de los países que juegan. 
        """
        countries = ""

        local_str = Team.get_name(self.local)
        visitante_str = Team.get_name(self.visitante)

        countries = local_str + " vs. " + visitante_str

        return countries

    def get_stadium(self): 
        return self.estadio

    def get_date(self): 
        return self.date

    def get_id(self): 
        return self.id_partido

    def get_taken_seats(self): 
        return self.taken_seats

    def get_info(self): 
        local_str = Team.get_name(self.local)
        visitante_str = Team.get_name(self.visitante)


        ##2-   England vs. Iran // 11/21/2022 16:00
        info = "#" + str(self.id_partido) + "-   " + local_str + " vs. " + visitante_str + " // " + str(self.date)
        return info

    def get_asistentes(self):
        return self.asistentes

    def get_vendido(self):
        return self.vendidos

    def new_venta(self): 
        self.vendidos += 1

    def new_asistente(self):
        self.asistentes += 1

    def new_taken_seat(self, seat): 
        self.taken_seats.append(seat)

