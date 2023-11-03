class TS:
    def cifrar_transposicion(self, mensaje, clave):
        clave_str = str(clave)  # Convertir la clave a una cadena de caracteres
        columnas = len(clave_str)
        filas = (len(mensaje) + columnas - 1) // columnas
        matriz = [[' ' for _ in range(columnas)] for _ in range(filas)]

        fila_actual, columna_actual = 0, 0
        for letra in mensaje:
            matriz[fila_actual][columna_actual] = letra
            columna_actual += 1
            if columna_actual == columnas:
                columna_actual = 0
                fila_actual += 1

        mensaje_cifrado = ''
        orden_clave = sorted(range(columnas), key=lambda x: clave_str[x])
        for columna in orden_clave:
            for fila in range(filas):
                mensaje_cifrado += matriz[fila][columna]

        return mensaje_cifrado

    def descifrar_transposicion(self, mensaje_cifrado, clave):
        clave_str = str(clave)  # Convertir la clave a una cadena de caracteres
        columnas = len(clave_str)
        filas = (len(mensaje_cifrado) + columnas - 1) // columnas
        matriz = [[' ' for _ in range(columnas)] for _ in range(filas)]

        orden_clave = sorted(range(columnas), key=lambda x: clave_str[x])

        letras_ultima_fila = len(mensaje_cifrado) % filas
        filas_completas = filas - letras_ultima_fila

        idx = 0
        for columna in orden_clave:
            if columna < letras_ultima_fila:
                for fila in range(filas):
                    matriz[fila][columna] = mensaje_cifrado[idx]
                    idx += 1
            else:
                for fila in range(filas_completas):
                    matriz[fila][columna] = mensaje_cifrado[idx]
                    idx += 1

        mensaje_descifrado = ''
        for fila in range(filas):
            for columna in range(columnas):
                mensaje_descifrado += matriz[fila][columna]

        return mensaje_descifrado.strip()

