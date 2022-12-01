from search import Search
from match import Match
from stadium import Stadium
from purchase import Purchase
import string
import random

def main_compra(lista_estadios, lista_partidos, lista_purchases, given_purchase_ids): 
    """Lleva todo el proceso de compra y de búsqueda. Se apoya en las demas funciones del módulo. Puedes buscar y luego comprar o puedes comprar de una. 

    Args:
        lista_estadios(list): lista de objetos Stadium
        lista_partidos(list): lista de objetos Match
        lista_purchases(list): lista de objetos Purchase
        given_purchase_ids(list): códigos de factura previamente dados, para que toda factura tenga un código único. 
    """    
    print("...................")
    print("COMPRAR ENTRADAS:")

    #Definimos si va a buscar estadio o va a comprar entradas. 
    while True: 
        opciones = input("""
        1. Buscar Partido: ver los partidos por país, fecha o estadio.

        2. Comprar Entrada: escoger un partido y comprar su entrada. 
        
        Seleccione: 
        """)

        if opciones == "1" or opciones == "2": 
            break
        else: 
            print("Respuesta incorrecta. ")
        
    if opciones == "1": 

        #Creamos un objeto Search que nos permitirá accesar a las funciones de búsqueda. 
        objeto = Search(lista_partidos, lista_estadios)

        #Manejamos un menú para buscar según los tres criterios. 
        while True: 
            filter = input("""
            
            Con base en qué criterio desea buscar: 
            1. Equipo
            2. Estadio
            3. Fecha
            """)

            if int(filter) in range(1, 4):
                break 
            else: 
                print("Opción inválida")

        if filter == "1": Search.search_by_country(objeto)
        elif filter == "2": Search.search_by_stadium(objeto)
        else: 
            Search.search_by_date(objeto)
    
    else: 
        lista_purchases = proceso(lista_partidos, lista_purchases, given_purchase_ids)

        pass



def proceso(lista_partidos, lista_purchases, given_purchase_ids):
    """Todo el proceso de compra

    Args:
        lista_partidos(list): lista de objetos Match
        lista_purchases(list): lista de objetos Purchase
        given_purchase_ids(list): códigos de factura previamente dados, para que toda factura tenga un código único. 

    Returns:
        list: lista de objetos Purchase modificada con el pedido adicional
    """    
    while True: 
        try:
            name = input("\n\nIngrese el nombre del usuario:    ")

            if not "".join(name.split()).isalpha():
                raise Exception 


            id = int(input("Ingrese su número de identificación:    "))
            if int(id) < 0: 
                raise Exception 

            age = int(input("Ingrese su edad:    "))
            if age < 0: 
                raise Exception 

            break


        except: 
            print("\n\tDatos del clientes inválidos. Por favor, ingrese de nuevo sus datos de forma correcta.\n")

    #Partido escogido
    selected_match = select_partido(lista_partidos)
    
    #Sector: VIP o General
    sector = escoger_tipo_entrada()

    #Estadio donde se juega. 
    selected_estadio = Match.get_stadium(selected_match)

    seat = pick_seat(selected_estadio, sector, selected_match)

    if sector == "General": 
        inicial = 50
    else: 
        inicial = 120

    descuento_por_vampiro = vampire(int(id))
    #Chequeamos si es vampiro. 

    if descuento_por_vampiro: 
        print("         DESCUENTO POR ID VAMPIRO (50%)")
        descuento = inicial/2
    else: 
        descuento = 0

    impuesto = inicial*0.16

    total = inicial + impuesto - descuento
    #Sacamos el total. 

    #Info del partido y nombre del estadio. 
    partido_str = Match.get_info(selected_match)
    estadio_str = Stadium.get_name(selected_estadio)


    #Se muestra una previa de la factura. A modo de confirmar la transaccion
    print("""

    --------------------
                Previsualización :
                - Partido: {}
                - Estadio: {}
                - Monto inicial: {}
                - Impuesto: {}
                - Descuento: {}
                - Monto final: {}    
    ----------------------

    """.format(partido_str, estadio_str, inicial, impuesto, descuento, total))



    while True: 
        validacion = input("""
                    1. Confirmar transacción.
                    2. Anular

        Ingrese elección:  """)
        
        if validacion != "1" and validacion != "2": 
            print("Dato erróneo")

        else: 
            break 

    #Imprimimos la factura. 
    if validacion == "1": 
        print("\t\t\tCOMPRA REALIZADA CON ÉXITO")

        consumo = []
        codigo = codigo_unico(given_purchase_ids)

        factura = Purchase(codigo, name, id, age, selected_match, sector, seat, total, consumo)

        #Aumentamos venta y ocupamos el asiento. 
        Match.new_venta(selected_match)
        Match.new_taken_seat(selected_match, seat)

        lista_purchases.append(factura)
        
        given_purchase_ids.append(codigo)

        Purchase.print_receipt(factura)

    
    else: 

        print("\nCompra anulada.\n")
    
    return lista_purchases
        

def codigo_unico(given_purchase_ids):
    """Da un número aleatorio que servirá de código de factura. Se comprueba que no haya sido asignado anteriormente. 

    Returns:
        int: numero
    """     

    while True:
        n = random.randint(1000, 9999)
        if n not in given_purchase_ids:
            break

    return n


def vampire(id): 
    """Define si un número es vampiro.

    Args:
        id (string): ID del usuario. 

    Returns:
        booleano: Verdadero o falso.
    """
    id_str = str(id)
    digitos = len(id_str)

    if digitos%2 != 0 or digitos == 2:
        return False

    for x in range(1, (int(id)//2 + 1)): 
        for y in range(1, (int(id)//2 + 1)): 
            if str(x)[-1] == 0 and str(y)[-1]== 0: 
                continue 
            
            if len(str(x)) + len(str(y)) != digitos: 
                continue
            
            if x*y==id: 
                return True
    
    return False


def pick_seat(estadio, sector, selected_match):
    """Se encarga de devolver el asiento. Para eso, se encarga de las matrices, de las VIP y la general e intercambia con el usuario para devoler el asiento.

    Args:
        estadio (Stadium): objeto Estadio, el del partido seleccionado.
        sector (string): VIP o General
        selected_match (Match): objeto Match

    Returns:
        seat(string): código del asiento A9, E3, D2
    """    
    capacidad = Stadium.get_capacidad(estadio)

    capacidad_total = sum(capacidad)

    matriz_completa = crear_matriz(capacidad_total)

    numero_filas_vip = capacidad[1]//10
    mvip = []
    mgral = []

    for i in range(0, numero_filas_vip):
        mvip.append(matriz_completa[i])

    for i in range(numero_filas_vip, len(matriz_completa)):
        mgral.append(matriz_completa[i])

    print("\n\n\n")

    if sector == "General": 
        print("\t\tMatriz de Asientos General\n")
        print_m(mgral)
        seat = select_seat(selected_match, estadio, mgral)
    else: 
        print("\t\tMatriz de Asientos VIP\n")
        print_m(mvip)
        seat = select_seat(selected_match, estadio, mvip)
    
    return seat

def select_seat(match, estadio, selected_matrix):
    """Se encarga de recibir el input del asiento. 

    Args:
        match (Match): objeto Partido
        estadio (Stadium): objeto Stadium
        selected_matrix (list): lista de listas, la matriz del sector de la entrada

    Returns:
        seat(string): código del asiento A9, E3, D2
    """    
    confirmation = False
    print("Asientos Ocupados: ")
    for seat in Match.get_taken_seats(match): 
        print("- " + seat)
    
    while True: 
        try: 

            seat = input("Escriba el código del asiento que desea:   ").upper()

            for line in selected_matrix:
                if seat in line:
                    confirmation = True
                    break 

            if not confirmation: raise Exception

            if seat in Match.get_taken_seats(match):
                raise Exception

            break 
        except:  
            print("El asiento ingresado no es válido o se encuentra ocupado.")

    return seat


def print_m(matrix):
    linea_str = "" #Volvemos cada línea un string, para imprimirlo en un solo movimiento quitándole el formato de lista.

    for line in matrix: 
        for seat in line: 
            linea_str += seat
            linea_str += "  " 
    
        print(linea_str)
        linea_str = ""

    print("")

def crear_matriz(capacidad):
    """se desarrolla una matriz de asientos, cada asiento tiene una letra y un número, por eso se utiliza la función del abecedario. 

    Args:
        capacidad (int): cantidad de asientos

    Returns:
        (list): lista de listas, una matriz.
    """
    abecedario = list(string.ascii_uppercase)
    #Buscamos las letras del abecedario en mayúscula con la librería importada. 
    
    #La capacidad son los asientos que tenemos que sacar. Lo haremos con filas de 10 asientos, todas las capacidades de todos los estadios son divisibles entre 10. 

    n_filas = capacidad//10 #número de filas que tendremos, con este número sacaremos las letras que utilizaremos. 

    filas_letras = []

    for i in range(0, n_filas): 
        filas_letras.append(abecedario[i])

    matrix = []

    for letra in filas_letras: 
        linea = [] #Creamos las líneas de asientos, letra y número. 
        for x in range(1,11): 
            linea.append(letra + str(x)) #Letra y número, del 1 al 11 porque será de 1 al 10.  
        matrix.append(linea)

    return matrix

def escoger_tipo_entrada():
    """Recibe las peticiones del cliente sobre los tipos de entrada. 

    Returns:
        boleto_type(str): General o VIP
    """
    print("\n\nTipos de Entrada: \n1. General: 50$ \n\t- Solo podrá ver el partido desde su asiento. \n\n2. VIP: 120$ \n\t- Podrá disfrutar del restaurante del estadio.    ")


    while True: 
        try:
            boleto_type = input("Ingrese el número de su selección:     ")

            if boleto_type != "1" and boleto_type != "2": 
                raise Exception
            
            break
    
        except:
            print("Por favor, ingrese una opción válida.")

    if boleto_type == "1": boleto_type = "General"
    else: boleto_type = "VIP"

    return boleto_type


def select_partido(lista_partidos):
    """Escoge el objeto Partido

    Args:
        lista_partidos (Match): lista de objeto Partido

    Returns:
        (Partido)
    """    
    for match in lista_partidos: 
        print("--------------------------------")
        Match.print_match(match) 

    while True: 
        try:
            match_id = int(input("Ingrese el número del partido de su escogencia:     "))

            if match_id not in range(1, 49): 
                raise Exception

            break 
        except: 
            print("Por favor, ingrese una opción válida.")

    for partido in lista_partidos:
        if Match.get_id(partido) == int(match_id):
            return partido