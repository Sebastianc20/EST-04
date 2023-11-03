from Model import ArbolAVL  # Importa la clase ArbolAVL desde el módulo Model
from TS import TS
import json
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


class Personas:
    def __init__(self, nombre, id_persona, fecha_nacimiento, direccion,companies):
        # Constructor de la clase Personas
        self.Nombre = nombre
        self.Id_Personas = id_persona
        self.Fecha_Nacimiento = fecha_nacimiento
        self.Direccion = direccion
        self.companies = companies
        
    
class RegistroPersonas:
    def __init__(self):
        # Constructor de la clase RegistroPersonas
        self.arbol_avl = ArbolAVL()  # Crea una instancia de tu Árbol AVL
        self.cartas_por_id = {}  # Un diccionario para mapear ID (DPI) a lista de cartas
        self.ts = TS()
        self.private_key = self.generar_clave_privada_rsa()

    def generar_clave_privada_rsa(self):
        # Generar una clave privada RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        return private_key

    def firmar_carta(self, contenido_carta):
        # Firmar digitalmente la carta
        hash_carta = hashlib.sha256(contenido_carta.encode('utf-8')).hexdigest()
        firma = self.private_key.sign(
            hash_carta.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return hash_carta, firma
    
    
    def insertar_persona(self, nombre, id_persona, fecha_nacimiento, direccion, companies):
        # Método para insertar una persona en el Árbol AVL
   
        persona = Personas(nombre, id_persona, fecha_nacimiento, direccion, companies)
        clave = (nombre, id_persona)
        self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, clave, persona)
        print(f"Persona insertada correctamente:")
        print(f"Nombre: {nombre}")
        print(f"DPI Comprimido: {id_persona}")
        print(f"Fecha de Nacimiento: {fecha_nacimiento}")
        print(f"Dirección: {direccion}")
        print(f"Empresas: {companies}")
        
        
    def eliminar_persona_por_nombre_id(self, nombre, id_persona):
        # Método para eliminar una persona del Árbol AVL por nombre e ID
        clave = (nombre, str(id_persona))  # Convierte id_persona a cadena de texto
        self.arbol_avl.raiz = self.arbol_avl.eliminar(self.arbol_avl.raiz, clave)  # Elimina la persona del Árbol AVL
             
    def buscar(self, nombre, id_persona):
            # Método para buscar registros en el Árbol AVL por nombre e ID
        registros = self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz, nombre, id_persona)
        return registros

    def buscar_dpi(self, id_persona):
        # Buscar registros en el árbol AVL por el DPI original (sin descomprimir)
        registros = self.arbol_avl.buscar_por_id_persona(self.arbol_avl.raiz, id_persona)
        return registros

    def buscar_registros_por_nombre(self, nombre, id_persona):
        # Método para buscar registros en el Árbol AVL por nombre e ID
        registros = self.arbol_avl.buscar_por_nombre_y_id(self.arbol_avl.raiz, nombre, id_persona)

        if registros:
            print("\nRegistros encontrados:")
            for registro in registros:
                persona_json = {
                    "name": registro.Nombre,
                    "dpi": registro.Id_Personas,  # Descomprimir y unir el DPI
                    "datebirth": registro.Fecha_Nacimiento,
                    "address": registro.Direccion,
                    "companies": registro.companies
                }
                json_str = json.dumps(persona_json)
                print(f"INSERT;{json_str}")
                self.buscar_cartas_de_persona(id_persona)
        else:
            print(f"No se encontraron registros para el nombre: {nombre}")
        return registros

    def actualizar_persona_por_nombre_id(self, nombre, id_persona, nueva_fecha_nacimiento, nueva_direccion, nuevas_empresas):
        # Método para actualizar los datos de una persona en el Árbol AVL por nombre e ID
        clave = (nombre, id_persona)  # Crea una clave única para la persona
                        
        #Comprobar si nuevas_empresas es None y asignar una lista vacía en su lugar
        if nuevas_empresas is None:
            nuevas_empresas = []        
        
        # Buscar la persona en el Árbol AVL
        persona = self.arbol_avl.actualizar_persona(self.arbol_avl.raiz, clave, nueva_fecha_nacimiento, nueva_direccion, nuevas_empresas)

        if persona is not None:
            # Actualizar los campos de la persona con los nuevos valores
            persona.Fecha_Nacimiento = nueva_fecha_nacimiento
            persona.Direccion = nueva_direccion
            persona.companies = nuevas_empresas


    def insertar_carta(self, id_persona, contenido_carta):
        # Calcular el hash del contenido original
        hash_carta = hashlib.sha256(contenido_carta.encode('utf-8')).hexdigest()
        
        # Cifrar el contenido de la carta utilizando transposición simple
        contenido_cifrado = self.ts.cifrar_transposicion(contenido_carta, id_persona)
        
        # Firmar el hash de la carta
        firma = self.firmar_carta(hash_carta)
        
        if id_persona not in self.cartas_por_id:
            self.cartas_por_id[id_persona] = []
        
        self.cartas_por_id[id_persona].append((contenido_cifrado, hash_carta, firma))
        
        print("Se ha agregado una Conversacion para la persona con ID:", id_persona)
        print("Contenido de la Conversacion cifrada:", contenido_cifrado)
        print("Hash de la Conversacion:", hash_carta)
        print("Firma generada:", firma)

    def buscar_cartas_de_persona(self, id_persona):
        # Buscar una persona por su ID (DPI)
        if id_persona in self.cartas_por_id:
            cartas = self.cartas_por_id[id_persona]
            for i, carta in enumerate(cartas, start=1):
                contenido_cifrado, hash_carta, firma = carta
                contenido_descifrado = self.ts.descifrar_transposicion(contenido_cifrado, id_persona)
                hash_actual = hashlib.sha256(contenido_descifrado.encode('utf-8')).hexdigest()
                if hash_actual == hash_carta:
                    print("Conversacion número:", i)
                    print("La Conversacion para la persona con ID:", id_persona, "es válida.")
                    print("Contenido de la Conversacion descifrada:", contenido_descifrado)
                else:
                    print("Conversacion número:", i)
                    print("La conversacion para la persona con ID:", id_persona, "ha sido modificada.")
                    print("Hash actual:", hash_actual)
                    print("Hash almacenado en la carta:", hash_carta)
                print("\n")  # Imprimir una línea en blanco para separar cada carta
        else:
            print("No se encontró una persona con el ID (DPI) especificado.")



# Crear una instancia de la clase RegistroPersonas
base_de_datos = RegistroPersonas()