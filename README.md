# Sonido estéreo y ficheros WAVE

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Ana Fernandez Tejero

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

### Registro de Validación Automatizada (`doctest`)
```text
Trying:
    cabecera_in = st.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 52, b'WAVE', b'fmt ', 16, 1, 2, 44100, 176400, 4, 16, b'data', 16)
Expecting nothing
ok
Trying:
    muestras_in = st.pack('<8h', 1000, 500, 2000, -1000, -500, 500, 0, 0)
Expecting nothing
ok
Trying:
    f_in = io.BytesIO(cabecera_in + muestras_in)
Expecting nothing
ok
Trying:
    f_out = io.BytesIO()
Expecting nothing
ok
Trying:
    codEstereo(f_in, f_out)
Expecting nothing
ok
Trying:
    _ = f_out.seek(0)
Expecting nothing
ok
Trying:
    meta = leer_cabecera(f_out)
Expecting nothing
ok
Trying:
    meta['num_channels'], meta['bits_per_sample']
Expecting:
    (1, 32)
ok
Trying:
    cabecera_in = st.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 52, b'WAVE', b'fmt ', 16, 1, 1, 44100, 176400, 4, 32, b'data', 16)
Expecting nothing
ok
Trying:
    muestras_cod = st.pack('<4I', ((750 & 0xFFFF) << 16) | (250 & 0xFFFF), ((500 & 0xFFFF) << 16) | (1500 & 0xFFFF), 0, 0)
Expecting nothing
ok
Trying:
    f_in = io.BytesIO(cabecera_in + muestras_cod)
Expecting nothing
ok
Trying:
    f_out = io.BytesIO()
Expecting nothing
ok
Trying:
    decEstereo(f_in, f_out)
Expecting nothing
ok
Trying:
    _ = f_out.seek(0)
Expecting nothing
ok
Trying:
    meta = leer_cabecera(f_out)
Expecting nothing
ok
Trying:
    meta['num_channels'], meta['bits_per_sample']
Expecting:
    (2, 16)
ok
Trying:
    archivo_virtual = io.BytesIO()
Expecting nothing
ok
Trying:
    escribir_cabecera(archivo_virtual, 1, 8000, 16, 200)
Expecting nothing
ok
Trying:
    _ = archivo_virtual.seek(0)
Expecting nothing
ok
Trying:
    meta = leer_cabecera(archivo_virtual)
Expecting nothing
ok
Trying:
    meta['num_channels'], meta['sample_rate'], meta['bits_per_sample'], meta['data_size']
Expecting:
    (1, 8000, 16, 200)
ok
Trying:
    datos_wav = st.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 44, b'WAVE', b'fmt ', 16, 1, 2, 44100, 176400, 4, 16, b'data', 8)
Expecting nothing
ok
Trying:
    archivo_virtual = io.BytesIO(datos_wav)
Expecting nothing
ok
Trying:
    meta = leer_cabecera(archivo_virtual)
Expecting nothing
ok
Trying:
    meta['num_channels'], meta['sample_rate'], meta['bits_per_sample']
Expecting:
    (2, 44100, 16)
ok
3 items had no tests:
    __main__
    __main__.estereo2mono
    __main__.mono2estereo
4 items passed all tests:
   8 tests in __main__.codEstereo
   8 tests in __main__.decEstereo
   5 tests in __main__.escribir_cabecera
   4 tests in __main__.leer_cabecera
25 tests in 7 items.
25 passed.
Test passed.

¡Validación completada con éxito! Procesando las pistas de audio definitivas...

[ÉXITO] Archivos creados correctamente siguiendo los requerimientos técnicos:
  - beatles_L.wav (Sección de voces y aplausos -> Canal 0)
  - beatles_R.wav (Sección instrumental -> Canal 1)
  - beatles_mono.wav (Combinación monofónica de semisuma)
  - beatles_semidiferencia.wav (Componente de semidiferencia / Atributos espaciales)
```

#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

##### Código de `estereo2mono()`
```python
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
```
##### Código de `mono2estereo()`
```python
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
```
##### Código de `codEstereo()`
```python
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
```
##### Código de `decEstereo()`
```python
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
```
#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
