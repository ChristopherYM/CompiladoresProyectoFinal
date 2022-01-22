# CompiladoresProyectoFinal

Alumno: Christopher Yquira Miranda

Descripción de implementación:

El trabajo cuanta con una función principal, la cual es el analizadorLexico y 3 funciones secundarias (reconoceAlphanum, reconoceString y reconoceNumero)
-analizadorLexico: recorre todo el archivo .txt y va llamando a las distintas funciones secundarias según sea lo que lea en cada iteración. Obviamente en cada caso se tienen en cuenta las palabras reservadas, los operadores, los delimitadores y los comentarios, saltos de línea y espacios.
- reconoceAlphanum: Se verifica que solo contenga letras y números, de no ser así seria un error de ID.
- reconoceString: Se verificamos que luego de un carácter '\'' siempre termine en otro y verifica la posibilidad de tener dos caracteres juntos.
- reconoceNumero: Se verifica que solo contenga números y que estos puedan ser int o float, solo si lleva un '.'.
Adicionalmente para facilitar el código, se crearon listas en las que se encuentran los operadores, delimitadores y las palabras reservadas. 

Para poder ejecutar el proyecto:

- Simplemente se debe ejecutar nuestro main del archivo "proyecto_final.py"
- No es necesario añadir alguna librería
- Dentro de la carpeta "codigoInputPrueba", se tiene un archivo "valido1.txt" en el cual podemos colocar el código a ser analizado por nuestro Escáner. (Actualmente el archivo .txt cuenta con "cadenas de pruebas" y "código prueba 2", las cuales fueron proporcionadas en clase. Esto con la finalidad de simplemente ejecutar el código)

