from team import Team
from product import Product
from stadium import Stadium 
from match import Match
import requests

def setting_equipos_all(): 
    """Agarra la información de la API y saca la base de datos de los equipos. 

    Args:
        json_equipos (list): lista de diccionarios desde la api

    Returns:
        equipos_all:  Lista de objetos Team. 
    """    

    url_equipos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json"

    json_equipos = descargar(url_equipos)

    equipos_all = []
    for equipo in json_equipos: 
        team = Team(equipo["name"], equipo["flag"] ,equipo["fifa_code"], equipo["group"], equipo["id"])

        equipos_all.append(team)

    return equipos_all


def setting_stadiums_all(): 
    """Agarra la información de la API y saca la base de datos de los estadios. 

    Args:
        json_equipos (): _description_

    Returns:
        equipos_all:  Lista de objetos Team. 
    """    

    url_estadios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json"

    json_estadios = descargar(url_estadios)

    stadiums_all = []
    
    productos_list_de_obj = []
    #Lista de diccionarios, 

    for estadio in json_estadios:
        for restaurante in estadio["restaurants"]: 
            for product in restaurante["products"]:
                p = Product(product["name"], product["quantity"], product["price"], product["type"], product["adicional"])
                productos_list_de_obj.append(p)

            restaurante["products"] = productos_list_de_obj
            productos_list_de_obj = []

        s = Stadium(estadio["id"], estadio["name"], estadio["capacity"], estadio["location"], estadio["restaurants"])
        stadiums_all.append(s)
    return stadiums_all


def setting_matches_all(equipos_all, stadiums_all, ):
    """Crea la base de datos de los partidos. Incluyendo su estadio, apoyándose en la base de datos de objetos Stadium. 

    Args:
        json_partidos (list): _description_
        stadiums_all (list): lista de objetos Stadium

    Returns:
        matches_all (list): lista de objetos Partido.
    """
    matches_all = []

    

    url_partidos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json"

    json_partidos = descargar(url_partidos)

    for partido in json_partidos:
        #Para estadio, tomamos el objeto estadio y para equipos tomamos los objetos equipo.

        estadio = stadiums_all[(partido["stadium_id"]) - 1]
    
        for equipo in equipos_all: 
            if Team.get_name(equipo) == partido["home_team"]: 
                e_local = equipo
            elif Team.get_name(equipo) == partido["away_team"]:
                e_visitante = equipo

        taken_seats=[]

        p = Match(e_local, e_visitante, partido["date"], estadio, int(partido["id"]), 0, 0, taken_seats)

        matches_all.append(p)

    return matches_all


def descargar(url): 
    """Hace request a APIs.
        json_equipos: lista de diccionarios desde la api.
        json_partidos: lista de diccionarios desde la api.
        json_estadios: lista de diccionarios desde la api.

        Return: (list): lista de diccionarios según la api
    """    

    response = requests.get(url)
    return response.json()


def print_all(teams_all, stadiums_all, matches_all):
    print("\n\nEQUIPOS: ")
    for team in teams_all: 
        Team.print_team(team)

    print("\n\nESTADIOS: ")
    for stadium in stadiums_all: 
        Stadium.print_stadium(stadium)
        #print(Stadium.get_restaurants(stadium))
        Stadium.print_restaurants(stadium)

    print("\n\nPARTIDOS: ")
    for match in matches_all: 
        Match.print_match(match)






