"""
Nombre: Ana Fernández Tejero
Descripción: Módulo para la manipulación de canales en ficheros WAVE y
codificación/decodificación de señales estéreo y mono.
"""
import struct as st
import io

def leer_cabecera(archivo):
    """
    >>> datos_wav = st.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 44, b'WAVE', b'fmt ', 16, 1, 2, 44100, 176400, 4, 16, b'data', 8)
    >>> archivo_virtual = io.BytesIO(datos_wav)
    >>> meta = leer_cabecera(archivo_virtual)
    >>> meta['num_channels'], meta['sample_rate'], meta['bits_per_sample']
    (2, 44100, 16)
    """
    buffer = archivo.read(12)
    if len(buffer) < 12: 
        raise ValueError("¡El archivo WAVE suministrado no está entero o está dañado!")

    id_fragmento, tamano_fragmento, formato_fragmento = st.unpack('4sI4s', buffer) 
    
    if id_fragmento != b'RIFF' or formato_fragmento != b'WAVE':
        raise ValueError("La cabecera no corresponde a un formato WAVE legítimo")

    id_subfragmento1 = archivo.read(4)  
    while id_subfragmento1 != b'fmt ':
        if len(id_subfragmento1) < 4:
            raise ValueError("No se localizó la sección esencial 'fmt'")
        tamano = st.unpack('<I', archivo.read(4))[0]
        archivo.seek(tamano, 1)  
        id_subfragmento1 = archivo.read(4)

    tamano_subfragmento1 = st.unpack('<I', archivo.read(4))[0]
    buffer_fmt = archivo.read(tamano_subfragmento1)

    formato_audio, num_canales, tasa_muestreo, tasa_bytes, alineacion_bloque, bits_por_muestra = st.unpack('<HHIIHH', buffer_fmt[:16])

    id_subfragmento2 = archivo.read(4)
    while id_subfragmento2 != b'data':
        if len(id_subfragmento2) < 4:
            raise ValueError("Falta el identificador 'data' en el archivo.")
        tamano = st.unpack('<I', archivo.read(4))[0]
        archivo.seek(tamano, 1)
        id_subfragmento2 = archivo.read(4)

    tamano_subfragmento2 = st.unpack('<I', archivo.read(4))[0]
    
    return {
        "chunk_size": tamano_fragmento,
        "num_channels": num_canales,
        "sample_rate": tasa_muestreo,
        "byte_rate": tasa_bytes,
        "block_align": alineacion_bloque,
        "bits_per_sample": bits_por_muestra,
        "data_size": tamano_subfragmento2
    }

    
def escribir_cabecera(archivo, num_canales, tasa_muestreo, bits_por_muestra, tamano_datos):
    """
    >>> archivo_virtual = io.BytesIO()
    >>> escribir_cabecera(archivo_virtual, 1, 8000, 16, 200)
    >>> _ = archivo_virtual.seek(0)
    >>> meta = leer_cabecera(archivo_virtual)
    >>> meta['num_channels'], meta['sample_rate'], meta['bits_per_sample'], meta['data_size']
    (1, 8000, 16, 200)
    """
    tamano_subfragmento1 = 16
    alineacion_bloque = (num_canales * bits_por_muestra) // 8
    tasa_bytes = tasa_muestreo * alineacion_bloque
    tamano_fragmento = 36 + tamano_datos

    archivo.write(st.pack('<4sI4s', b'RIFF', tamano_fragmento, b'WAVE'))
    archivo.write(st.pack('<4sI', b'fmt ', tamano_subfragmento1))
    archivo.write(st.pack('<HHIIHH', 1, num_canales, tasa_muestreo, tasa_bytes, alineacion_bloque, bits_por_muestra))
    archivo.write(st.pack('<4sI', b'data', tamano_datos))


def estereo2mono(archivo_estereo, archivo_mono, canal=2):
    buffer = archivo_estereo.read(12) if hasattr(archivo_estereo, 'read') else None
    if buffer is not None:
        archivo_virtual_entrada = archivo_estereo
        archivo_virtual_entrada.seek(0)
        f_entrada = archivo_virtual_entrada
    else:
        f_entrada = open(archivo_estereo, 'rb')

    try:
        meta = leer_cabecera(f_entrada)
        if meta["num_channels"] != 2 or meta["bits_per_sample"] != 16:
            raise ValueError("Se requiere una pista estéreo codificada a 16 bits como origen")

        num_muestras = meta["data_size"] // 2  
        buffer = f_entrada.read(meta["data_size"])
        muestras = st.unpack(f'<{num_muestras}h', buffer)
    finally:
        if buffer is None:
            f_entrada.close()

    izquierdo = muestras[::2]
    derecho = muestras[1::2]

    if canal == 0:
        muestras_mono = izquierdo  
    elif canal == 1:
        muestras_mono = derecho  
    elif canal == 2:
        muestras_mono = [int((izq + der) / 2) for izq, der in zip(izquierdo, derecho)]
    elif canal == 3:
        muestras_mono = [int((izq - der) / 2) for izq, der in zip(izquierdo, derecho)]
    else:
        raise ValueError("Opción de canal errónea. Indique un valor de 0 a 3.")

    nuevo_tamano_datos = len(muestras_mono) * 2
    
    if hasattr(archivo_mono, 'write'):
        escribir_cabecera(archivo_mono, 1, meta["sample_rate"], 16, nuevo_tamano_datos)
        archivo_mono.write(st.pack(f'<{len(muestras_mono)}h', *muestras_mono))
    else:
        with open(archivo_mono, 'wb') as f_salida:
            escribir_cabecera(f_salida, 1, meta["sample_rate"], 16, nuevo_tamano_datos)
            f_salida.write(st.pack(f'<{len(muestras_mono)}h', *muestras_mono))


def mono2estereo(archivo_izquierdo, archivo_derecho, archivo_estereo):
    if hasattr(archivo_izquierdo, 'read') and hasattr(archivo_derecho, 'read'):
        f_izq = archivo_izquierdo
        f_der = archivo_derecho
        f_izq.seek(0)
        f_der.seek(0)
        cerrar = False
    else:
        f_izq = open(archivo_izquierdo, 'rb')
        f_der = open(archivo_derecho, 'rb')
        cerrar = True

    try:
        meta_izq = leer_cabecera(f_izq)
        meta_der = leer_cabecera(f_der)

        if meta_izq["num_channels"] != 1 or meta_der["num_channels"] != 1:
            raise ValueError("Ambos ficheros de origen deben poseer un único canal")
        if meta_izq["sample_rate"] != meta_der["sample_rate"]:
            raise ValueError("Las frecuencias de muestreo de los canales mono deben coincidir.")

        muestras_izq = st.unpack(f"<{meta_izq['data_size'] // 2}h", f_izq.read())
        muestras_der = st.unpack(f"<{meta_der['data_size'] // 2}h", f_der.read())
    finally:
        if cerrar:
            f_izq.close()
            f_der.close()

    longitud_minima = min(len(muestras_izq), len(muestras_der))
    muestras_estereo = [muestra for pareja in zip(muestras_izq[:longitud_minima], muestras_der[:longitud_minima]) for muestra in pareja]

    nuevo_tamano_datos = len(muestras_estereo) * 2
    
    if hasattr(archivo_estereo, 'write'):
        escribir_cabecera(archivo_estereo, 2, meta_izq["sample_rate"], 16, nuevo_tamano_datos)
        archivo_estereo.write(st.pack(f'<{len(muestras_estereo)}h', *muestras_estereo))
    else:
        with open(archivo_estereo, 'wb') as f_salida:
            escribir_cabecera(f_salida, 2, meta_izq["sample_rate"], 16, nuevo_tamano_datos)
            f_salida.write(st.pack(f'<{len(muestras_estereo)}h', *muestras_estereo))


def codEstereo(archivo_estereo, archivo_codificado):
    """
    >>> cabecera_in = st.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 52, b'WAVE', b'fmt ', 16, 1, 2, 44100, 176400, 4, 16, b'data', 16)
    >>> muestras_in = st.pack('<8h', 1000, 500, 2000, -1000, -500, 500, 0, 0)
    >>> f_in = io.BytesIO(cabecera_in + muestras_in)
    >>> f_out = io.BytesIO()
    >>> codEstereo(f_in, f_out)
    >>> _ = f_out.seek(0)
    >>> meta = leer_cabecera(f_out)
    >>> meta['num_channels'], meta['bits_per_sample']
    (1, 32)
    """
    if hasattr(archivo_estereo, 'read'):
        f_entrada = archivo_estereo
        f_entrada.seek(0)
        cerrar = False
    else:
        f_entrada = open(archivo_estereo, 'rb')
        cerrar = True

    try:
        meta = leer_cabecera(f_entrada)
        if meta["num_channels"] != 2 or meta["bits_per_sample"] != 16:
            raise ValueError("El archivo musical de origen obligatoriamente debe ser estéreo de 16 bits.")

        num_muestras = meta["data_size"] // 2
        muestras = st.unpack(f'<{num_muestras}h', f_entrada.read())
    finally:
        if cerrar:
            f_entrada.close()

    izquierdo = muestras[::2]
    derecho = muestras[1::2]

    muestras_codificadas = [
        ((int((izq + der) / 2) & 0xFFFF) << 16) | (int((izq - der) / 2) & 0xFFFF)
        for izq, der in zip(izquierdo, derecho)
    ]

    buffer_bytes = st.pack(f'<{len(muestras_codificadas)}I', *muestras_codificadas)

    if hasattr(archivo_codificado, 'write'):
        escribir_cabecera(archivo_codificado, 1, meta["sample_rate"], 32, len(buffer_bytes))
        archivo_codificado.write(buffer_bytes)
    else:
        with open(archivo_codificado, 'wb') as f_salida:
            escribir_cabecera(f_salida, 1, meta["sample_rate"], 32, len(buffer_bytes))
            f_salida.write(buffer_bytes)


def decEstereo(archivo_codificado, archivo_estereo):
    """
    >>> cabecera_in = st.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 52, b'WAVE', b'fmt ', 16, 1, 1, 44100, 176400, 4, 32, b'data', 16)
    >>> muestras_cod = st.pack('<4I', ((750 & 0xFFFF) << 16) | (250 & 0xFFFF), ((500 & 0xFFFF) << 16) | (1500 & 0xFFFF), 0, 0)
    >>> f_in = io.BytesIO(cabecera_in + muestras_cod)
    >>> f_out = io.BytesIO()
    >>> decEstereo(f_in, f_out)
    >>> _ = f_out.seek(0)
    >>> meta = leer_cabecera(f_out)
    >>> meta['num_channels'], meta['bits_per_sample']
    (2, 16)
    """
    if hasattr(archivo_codificado, 'read'):
        f_entrada = archivo_codificado
        f_entrada.seek(0)
        cerrar = False
    else:
        f_entrada = open(archivo_codificado, 'rb')
        cerrar = True

    try:
        meta = leer_cabecera(f_entrada)
        if meta["num_channels"] != 1 or meta["bits_per_sample"] != 32:
            raise ValueError("Se precisa un archivo con estructura mono de 32 bits.")

        num_muestras = meta["data_size"] // 4
        muestras_32 = st.unpack(f'<{num_muestras}I', f_entrada.read())
    finally:
        if cerrar:
            f_entrada.close()

    def a_int16(valor):
        return valor if valor < 0x8000 else valor - 0x10000

    semisuma = [a_int16(valor >> 16) for valor in muestras_32]
    semidiferencia = [a_int16(valor & 0xFFFF) for valor in muestras_32]

    izquierdo = [s + d for s, d in zip(semisuma, semidiferencia)]
    derecho = [s - d for s, d in zip(semisuma, semidiferencia)]

    muestras_estereo = [muestra for pareja in zip(izquierdo, derecho) for muestra in pareja]

    nuevo_tamano_datos = len(muestras_estereo) * 2
    
    if hasattr(archivo_estereo, 'write'):
        escribir_cabecera(archivo_estereo, 2, meta["sample_rate"], 16, nuevo_tamano_datos)
        archivo_estereo.write(st.pack(f'<{len(muestras_estereo)}h', *muestras_estereo))
    else:
        with open(archivo_estereo, 'wb') as f_salida:
            escribir_cabecera(f_salida, 2, meta["sample_rate"], 16, nuevo_tamano_datos)
            f_salida.write(st.pack(f'<{len(muestras_estereo)}h', *muestras_estereo))


if __name__ == "__main__":
    import doctest
    resultado_tests = doctest.testmod(verbose=True)
    
    if resultado_tests.failed == 0:
        print("\n¡Validación completada con éxito! Procesando las pistas de audio definitivas...")
        fichero_entrada = "Komm_gib_mir_deine_Hand.wav.wav" 
        
        try:
            estereo2mono(fichero_entrada, "beatles_L.wav", canal=0)
            estereo2mono(fichero_entrada, "beatles_R.wav", canal=1)
            estereo2mono(fichero_entrada, "beatles_mono.wav", canal=2)
            estereo2mono(fichero_entrada, "beatles_semidiferencia.wav", canal=3)
            
            print("\n[ÉXITO] Archivos creados correctamente siguiendo los requerimientos técnicos:")
            print("  - beatles_L.wav (Sección de voces y aplausos -> Canal 0)")
            print("  - beatles_R.wav (Sección instrumental -> Canal 1)")
            print("  - beatles_mono.wav (Combinación monofónica de semisuma)")
            print("  - beatles_semidiferencia.wav (Componente de semidiferencia / Atributos espaciales)")
            
        except FileNotFoundError:
            print(f"\n[FALTOU] Imposible localizar el archivo fuente especificado: '{fichero_entrada}'.")