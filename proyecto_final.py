dolar='$'

DiccionarioError={1:'Error lexico: No se encontro comilla de cierre en string',\
                  2:'Error lexico: Uso no permitido de caracter (\\)',\
                  3:'Error lexico: Error de escritura en valor numerico',\
                  4:'Error lexico: Error de escritura en nombre de variable',\
                  5:'Error lexico: Operador o caracter no reconocido',\
                  6:'Error sintactico: Falta operador llave ({) que indique inicio del Scope',\
                  7:'Error sintactico: Falta operador llave (}) que indique final del Scope',\
                  8:'Error sintactico: Falta operador punto y coma (;) que indique fin de linea'}
class Log:
    lista_errores=[]
    lista_warnigs=[]
    f=None
    def inicializar(self):
        self.lista_errores=[]
        self.lista_warnigs=[]
        self.f = open("errores.txt", "w")
    def addError(self, codigo, errorParametro):
        self.lista_errores.append( (errorParametro.indice,codigo) )
        self.f.write("Error "+str(codigo) +" en la linea "+str(errorParametro.indice[1]) +", posicion "+str(errorParametro.indice[0])+ "\nToken:" +errorParametro.palabra+"\n"+str(DiccionarioError[codigo])+"\n")
    def addWarning(self, codigo, warningParametro):
        self.lista_warnigs.append( (warningParametro.indice,codigo) )
        self.f.write("Warning "+str(codigo) +" en la linea "+str(warningParametro.indice[1]) +", posicion "+str(warningParametro.indice)+ "\nToken:" +warningParametro.palabra+"\n"+str(DiccionarioError[codigo])+"\n")
    def print(self):
        if(len(self.lista_errores)==0 and len(self.lista_warnigs)==0):
            return True
        self.f.close()
        f = open('errores.txt', 'r')
        file_contents = f.read()
        print (file_contents)
        f.close()
        return False
    def cerrarLog(self):
        self.f.close()

errorLog=Log()

delimitadores={',':"COMA",';':"PUNTO_COMA",':':"DOS_PUNTOS",'(':"OPEN_PARENTESIS",')':"END_PARENTESIS",\
               '[':"OPEN_CORCHETE",']':"END_CORCHETE",'..':"DELIMITADOR"}
operadores={"+":"SUMA","-":"RESTA","*":"MULTIPLICAR","/":"DIVIDIR","=":"IGUAL","<":"MENOR",\
            ">":"MAYOR","^":"OPERACIÓN","and":"AND","or":"OR","not":"NOT","div":"DIV","mod":"MOD","in":"IN"}
reservadas={"array","downto","function","of","repeat","until",\
            "begin","else","goto","packed","set","var","case","end","if",\
            "procedure","then","while","const","file","label","program","to",\
            "with","do","for","nil","record","type"}

class Token:
    palabra = "" #almacena una copia de la palabra
    indice = (-1,-1) #en donde apareció en la sentencia
    tipo = '' 
    def __init__(self,cadena, i, iLinea, t):
        self.palabra=cadena
        self.indice=(i,iLinea)
        self.tipo=t
    def toString(self):
        return "Pos_Token = "+str(self.indice)+"   <"+self.tipo+", "+self.palabra+">"

def reconoceNumero(linea,idx,lineaIdx):
    palabra=linea[idx]
    iAux=idx+1
    contPuntos=0
    while(iAux<len(linea) and linea[iAux]!=' ' and linea[iAux]!='\n' and linea [iAux]!= '\t'and linea[iAux] not in operadores and linea[iAux] not in delimitadores):
        if (linea[iAux]=='.'): #si es float 
            if (not linea[iAux+1].isdigit()):
                contPuntos=10
            else:
                contPuntos+=1
        elif (not linea[iAux].isdigit()): #error
            contPuntos=10
        palabra+=linea[iAux]
        iAux=iAux+1
    if(contPuntos == 0 and palabra[0] != '+'):
        return Token(palabra,idx,lineaIdx,'NUM_INT'),iAux
    elif(contPuntos == 1 and palabra[0] != '+'):
        return Token(palabra,idx,lineaIdx,'NUM_FLOAT'),iAux
    else:
        return Token(palabra,idx,lineaIdx,'ERROR_NUM'),iAux

def reconoceAlphanum(linea,idx,lineaIdx):
    iAux=idx
    palabra=""
    flagReconocer=True
    while(iAux<len(linea) and linea[iAux]!=' ' and linea[iAux]!='\n' and linea [iAux]!= '\t' and linea[iAux] not in operadores and linea[iAux] not in delimitadores):
        palabra+=linea[iAux]
        if((not linea[iAux].isalnum())): #es alfanum 
            flagReconocer=False
        iAux=iAux+1
    if(flagReconocer):
        if(palabra in reservadas):
            return Token(palabra,idx,lineaIdx,palabra.upper()),iAux
        elif (palabra in operadores):
            return Token(palabra,idx,lineaIdx,palabra.upper()),iAux
        else:
            return Token(palabra,idx,lineaIdx,'ID'),iAux
    else:
        return Token(palabra,idx,lineaIdx,'ERROR_ID'),iAux

def reconoceString(linea,idx,lineaIdx):
    iAux=idx+1
    texto='\''
    flagSlash=0
    while(iAux<len(linea) and linea[iAux]!='\''):
        texto+=linea[iAux]
        iAux=iAux+1
        if (linea[iAux]=='\'' and linea[iAux+1]=='\''):
            texto=texto+linea[iAux]+linea[iAux+1]
            iAux=iAux+2
        if (linea[iAux]=='\n'):
            flagSlash=1
            break
    if(flagSlash):
        return Token(texto+"\'",idx,lineaIdx,'ERROR_STRING'),idx+1
    elif(iAux<len(linea)):
        return Token(texto+"\'",idx,lineaIdx,'STRING'),iAux+1
    else:
        return Token("\'",idx,lineaIdx,'ERROR_STRING'),idx+1

def analizadorLexico(texto):
    tokens=[]
    lineaIdx=0
    for linea in texto:
        lineaIdx+=1
        idx=0
        while idx<len(linea):
            if linea[idx] == '\'':
                token,idx=reconoceString(linea,idx,lineaIdx)
                if token.tipo=='ERROR_STRING':
                    errorLog.addError(1,token)
                    token.tipo='string'
                tokens.append(token)
            elif ((linea[idx] == '+' or linea[idx] == '-') and linea[idx+1].isnumeric()) or linea[idx].isnumeric():
                token,idx=reconoceNumero(linea,idx,lineaIdx)
                if token.tipo=='ERROR_NUM':
                    errorLog.addError(3,token)
                    token.tipo=''
                tokens.append(token)
            elif linea[idx].isalpha():
                token,idx=reconoceAlphanum(linea,idx,lineaIdx)
                if token.tipo=='ERROR_ID':
                    errorLog.addError(4,token)
                    token.tipo='ID'
                tokens.append(token)
            elif linea[idx] in operadores: #operadores
                tokens.append(Token(linea[idx],idx,lineaIdx,operadores[linea[idx]]))
                idx=idx+1
            elif (linea[idx] == '(' and linea[idx+1] == '*'): #comentario
                idx=idx+2
                while (linea[idx] != '*' or linea[idx+1] != ')' and idx+2<len(linea)):
                    idx=idx+1
                idx=idx+2
            elif linea[idx] in delimitadores: #delimitadores
                tokens.append(Token(linea[idx],idx,lineaIdx,delimitadores[linea[idx]]))
                idx=idx+1
            elif (linea[idx] == ' ' or linea[idx]=='\t' or linea[idx]=='\n'): #esacio y salto de linea
                idx=idx+1
            elif linea[idx] == '{': #comentario
                while (linea[idx] != '}' and idx+1<len(linea)):
                    idx=idx+1
                idx=idx+1
            else:
                tokens.append(Token(linea[idx],idx,lineaIdx,'ERROR_LEXICO'))
                errorLog.addError(5,token)
                idx=idx+1
    return tokens

class Produccion:
    izq=""
    der=[]
    def __init__(self,i,d):
        self.izq=i
        self.der=d
    def getString(self):
        return self.izq+" -> "+' '.join(map(str, self.der))

class TAS:
    tablaSintactica={}
    terminales=[]
    noterminales=[]
    def __init__(self,gram):
        self.terminales=list(gram.terminales)
        #self.terminales.append("$")
        self.noterminales=list(gram.noterminales)
        for nT in self.noterminales:
            self.tablaSintactica[nT]={}
            for t in self.terminales:
                self.tablaSintactica[nT][t]=[]
        self.terminales.sort()
        self.noterminales.sort()
    def llenarEstaticamente(self,gram):
        self.terminales=list(gram.terminales)
        self.noterminales=list(gram.noterminales)
        for nT in gram.noterminales:
            self.tablaSintactica[nT]={}
            for t in gram.terminales:
                self.tablaSintactica[nT][t]=[]
        for p in gram.produccion:
            self.tablaSintactica[p.izq][p.der[0]]=p.der
        self.terminales.sort()
        self.noterminales.sort()
        #print(self.tablaSintactica)
    def print(self):
        aux='\t|'
        for t in self.terminales:
            if t!="lambda":
                aux+=t+'\t|'
        print (aux)
        for nT in self.noterminales:
            aux=nT+'\t|'
            for t in self.terminales:
                aux+=' '.join(map(str, self.tablaSintactica[nT][t]))
                aux+='\t|'
            print (aux)

class Nodo:
    etiqueta = ''
    hijos = []
    padre = None
    siguiente = None

    def __init__(self,etiqueta,padre):
        self.etiqueta=etiqueta
        self.padre=padre
        self.hijos=[]
        self.siguiente = None
    def imprimir(self):
        pivote=self
        while(True):
            if(len(pivote.hijos)>0):
                print(pivote.etiqueta,"->",end='')
                for h in pivote.hijos:
                    print(" ",h.etiqueta,end='')
                print()
            if(len(pivote.hijos)>0):
                pivote=pivote.hijos[0]
                #print(11111111)
            elif(pivote.siguiente!=None):
                pivote=pivote.siguiente
                #print(22222222)
            else:
                #print(33333333)
                while(pivote.siguiente==None):
                    if(pivote.padre==None):
                        return
                    pivote=pivote.padre
                pivote=pivote.siguiente


def opera1(pivote, literales):
    for l in reversed(literales):
        pivote.hijos.insert(0,Nodo(l,pivote))
        #print(pivote,pivote.hijos)
        #print(pivote.hijos[0],pivote.hijos[0].hijos)
        if(len(pivote.hijos)>1):
            pivote.hijos[0].siguiente=pivote.hijos[1]
    return pivote.hijos[0]

def opera2(pivote):
    if(pivote.siguiente!=None):
        return pivote.siguiente
    while(pivote.padre!=None):
        if(pivote.padre.siguiente!=None):
            return pivote.padre.siguiente
        else:
            pivote=pivote.padre
    return None
        
def opera3(pivote):

    pivote.hijos.append(Nodo('lambda',pivote))
    return opera2(pivote)


class Gramatica:
    produccion = [] #Lista de producciones
    terminales = set("$") #Conjunto de terminales
    noterminales = set() #no terminales
    inicial = ""
    primeros={}
    siguientes = {}
    tas=0
    def print(self): #Crear una función para imprimir
        for p in self.produccion:
            print (p.getString())
    def cargar(self,texto):
        for linea in texto:
            izqProdTemp =""
            strTemp = ""
            derProdTemp =[]
            idx=0
            while idx<len(linea):
                if (linea[idx]==':' and linea[idx+1]=='='):
                    izqProdTemp = strTemp
                    self.noterminales.add(strTemp)
                    if self.inicial=="":
                        self.inicial=strTemp
                    strTemp=""
                    idx+=1
                elif (linea[idx]=='|'):
                    if(len(strTemp)):
                        derProdTemp.append(strTemp)
                    self.produccion.append(Produccion(izqProdTemp,derProdTemp))
                    derProdTemp =[]
                elif (linea[idx]==' ' or linea[idx]=='\t' or linea[idx]=='\n'):
                    if (len(izqProdTemp) and len(strTemp)):
                        derProdTemp.append(strTemp)
                        self.terminales.add(strTemp)
                        strTemp=""
                else:
                    strTemp+=linea[idx]
                idx+=1
            if(len(strTemp)):
                derProdTemp.append(strTemp)
                self.terminales.add(strTemp)
            self.produccion.append(Produccion(izqProdTemp,derProdTemp))
            izqProdTemp =""
            derProdTemp =[]
        for e in self.noterminales:
            if e in self.terminales:
                self.terminales.remove(e)
        #Descomentar para ver primeros y siguientes
        print("terminales: ", self.terminales)
        print("no terminales: ", self.noterminales)
    def getProduccion(self,izq):
        aux=""
        for p in self.produccion:
            if (p.izq==izq):
                aux+=" | "*(len(aux)>0)+ p.der
        return aux
    def getProducciones(self,izq):
        aux=[]
        for p in self.produccion:
            if (p.izq==izq):
                aux.append( p.der)
        return aux
    def printProducciones(self):
        for p in self.produccion:
            print(p.getString())
    def getPrimero(self,izq):
        producciones = self.getProducciones(izq)
        primeros=set()
        primNoTerm=[]
        for p in producciones:
            if p[0] in self.terminales:
                primeros.add( p[0])
            elif p[0] not in primNoTerm:
                primNoTerm.append( p[0])
        for nT in primNoTerm:
            producciones = self.getProducciones(nT)
            for p in producciones:
                if p[0] in self.terminales:
                    primeros.add( p[0])
                elif p[0] not in primNoTerm:
                    primNoTerm.append( p[0])
        return primeros       
    def getPrimeros(self):
        self.primeros={}
        for nodo in self.noterminales:
            self.primeros[nodo]=self.getPrimero(nodo)
        return self.primeros
    def getSiguientes(self):
        
        self.siguientes = {}
        for nT in self.noterminales:
            self.siguientes[nT] = set()
        self.siguientes[self.inicial] = {dolar}
        self.getPrimeros()
        for r in range(5):
            for p in self.produccion:
                for i in range(len(p.der)-1):
                    if p.der[i] in self.noterminales:
                        if p.der[i+1] in self.noterminales:
                            self.siguientes[p.der[i]].update(self.primeros[p.der[i+1]])
                            if "lambda" in self.primeros[p.der[i+1]]:
                                self.siguientes[p.der[i]].remove("lambda")
                        else:
                            self.siguientes[p.der[i]].add(p.der[i+1])
                if p.der[len(p.der)-1] in self.noterminales:
                    self.siguientes[p.der[len(p.der)-1]].update(self.siguientes[p.izq])
        return self.siguientes
    def buscarProduccion(self, nodoNt, nodoT):
        prod=self.getProducciones(nodoNt)
        for p in prod:
            if (p[0] in self.terminales and p[0]==nodoT) or (p[0] in self.noterminales and nodoT in self.primeros[p[0]]):
                return p
        return []
    def buscarProduccionProximaBool(self, nodoNt, nodoT):
        prod=self.getProducciones(nodoNt)
        for p in prod:
            if (p[0] == nodoT):
                return True
        return False
    def crearTabla(self):
        print("siguientes: ", self.getSiguientes())
        self.getSiguientes()
        self.tas = TAS(self)
        for nodoNt in self.noterminales:
            for nodoT in self.primeros[nodoNt]:
                if nodoT != "lambda":
                    self.tas.tablaSintactica[ nodoNt ][ nodoT ] = self.buscarProduccion( nodoNt, nodoT)
                else:
                    for nodoT2 in self.siguientes[nodoNt]:
                        self.tas.tablaSintactica[nodoNt][nodoT2] = ["lambda"]
        #Descomentar para visualizar tabla
        self.tas.print()
        return self.tas

def analizar(gramatica, tokens ):
    contador=0
    pila=[]
    cola=[]
    raiz=Nodo(gramatica.inicial,None)
    pivote=raiz
    for t in tokens:
        cola.append(t.tipo)
    cola.append('$')
    pila.insert(0,'$')
    pila.insert(0,gramatica.inicial)
    print()
    #print("Tabla analisis sintactico:")
    #print("Pila"+' '*36+"Entrada"+' '*33+"Operacion"+'\t'+"Adicionar")
    while(len(cola) and len(pila)):
        auxPila=' '.join(map(str, reversed(pila)))
        auxCola=' '.join(map(str, cola))
        #raiz.imprimir()
        #print(auxPila+' '*(40-len(auxPila))+auxCola+' '*(40-len(auxCola)),end='')
        if(cola[0]==pila[0]):
            if(cola[0]!='$'):
                #print('2')
                pivote.val=tokens[contador].palabra
                pivote=opera2(pivote)
            else:
                print()
            cola.pop(0)
            pila.pop(0)
            contador+=1
                
        elif(pila[0] in gramatica.noterminales and cola[0] in gramatica.terminales):
            tmp=pila.pop(0)
            copiatmp=tmp
            if(copiatmp[0:5]=="Error"):
                print("Modo Panico Activado: Desvalance en parentesis")
                if(tmp=="ErrorIniScope"):
                    errorLog.addError(6,tokens[contador])
                elif(tmp=="ErrorEndScope"):
                    errorLog.addError(7,tokens[contador])
                elif(tmp=="ErrorEndLine"):
                    errorLog.addError(8,tokens[contador])
                return False
            elif len(gramatica.tas.tablaSintactica[tmp][cola[0]])>0:
                if gramatica.tas.tablaSintactica[tmp][cola[0]][0]=="lambda":
                    if gramatica.buscarProduccionProximaBool(tmp,'lambda'):
                        #print(len(gramatica.buscarProduccion(tmp,'lambda')))
                        pivote=opera3(pivote)
                    else:
                        pivote=opera1(pivote,gramatica.buscarProduccion(tmp,'lambda'))
                        for t in reversed(gramatica.buscarProduccion(tmp,'lambda')):
                            pila.insert(0,t)
                else:
                    pivote=opera1(pivote,gramatica.tas.tablaSintactica[tmp][cola[0]])
                    for t in reversed(gramatica.tas.tablaSintactica[tmp][cola[0]]):
                        pila.insert(0,t)
            elif gramatica.buscarProduccionProximaBool(tmp,'lambda'):
                #print('\n\n\n\n\n'+str(len(gramatica.buscarProduccion(tmp,'lambda')))+'\n\n\n\n\n\n')
                pivote=opera3(pivote)
            elif gramatica.buscarProduccion(tmp,'lambda'):
                pivote=opera1(pivote,gramatica.buscarProduccion(tmp,'lambda'))
                for t in reversed(gramatica.buscarProduccion(tmp,'lambda')):
                    pila.insert(0,t)
            else:
                print()
                print("Modo Panico Activado: No correspondencia con la gramatica")
                return False
        else:
            print()
            print("Modo Panico Activado: No correspondencia con la gramatica")
            return False
    print()
    print("Arbol sintactico generado:")
    raiz.imprimir()
    return True


###########################################################3


def main():
    gramaticaEditor=Gramatica()
    gramaticaEditor.cargar(open("gramatica.txt","r"))
    tabla = gramaticaEditor.crearTabla()
    errorLog.inicializar()
    tokens = analizadorLexico(open("codigoInputPrueba/valido1.txt","r"))
    arbolraiz=analizar(gramaticaEditor, tokens)

    if ( analizar(gramaticaEditor,tokens) and errorLog.print()):
        print("-------- codigo analizado con exito --------")
    else:
        print("-------- Error Semantico en code1 --------")
    errorLog.print()
    errorLog.f.close()
    
main()
