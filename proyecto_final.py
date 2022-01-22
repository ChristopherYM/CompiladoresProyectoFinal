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
                tokens.append(token)
            elif ((linea[idx] == '+' or linea[idx] == '-') and linea[idx+1].isnumeric()) or linea[idx].isnumeric():
                token,idx=reconoceNumero(linea,idx,lineaIdx)
                tokens.append(token)
            elif linea[idx].isalpha():
                token,idx=reconoceAlphanum(linea,idx,lineaIdx)
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
                idx=idx+1
    return tokens

def main():
    tokens = analizadorLexico( open("codigoInputPrueba/valido1.txt","r")) 

    for token in tokens:
        print(token.toString())
    
main()