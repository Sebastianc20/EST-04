class LZWCompressor:
    def __init__(self):
        self.reset_dictionary()

    def reset_dictionary(self):   # Reiniciar el diccionario para una nueva compresión
        self.dictionary = {}
        for i in range(256):
            self.dictionary[chr(i)] = i
        self.next_code = 256

    def compress(self, data):
        self.reset_dictionary()  
        result = []
        buffer = ""
        for char in data:
            new_buffer = buffer + char
            if new_buffer in self.dictionary:
                buffer = new_buffer
            else:
                result.append(self.dictionary[buffer])
                self.dictionary[new_buffer] = self.next_code
                self.next_code += 1
                buffer = char
        if buffer:
            result.append(self.dictionary[buffer])
        return result

    def decompress(self, data):
        dictionary = {i: chr(i) for i in range(256)}
        next_code = 256
        result = []
        buffer = chr(data[0])
        result.append(buffer)
        for code in data[1:]:
            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = buffer + buffer[0]
            else:
                entry = buffer + buffer[0]
            result.append(entry)
            dictionary[next_code] = buffer + entry[0]
            next_code += 1
            buffer = entry
        return''.join(result)
