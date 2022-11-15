import sys
import getopt

if __name__ == '__main__':
    o=''
    n=''
    m=''

    (opt,arg) = getopt.getopt(sys.argv[1:], 'o:n:m', ["operador=", "primernumero=", "segundonumero="])
    print("opciones: ", opt)
    print("argumentos: ", arg)

    for (op,ar) in opt:
        if(op in ['-o', '-n', '-m',"--operador=", "--primernumero=", "--segundonumero="]):
            if op== '-o':
                o = ar
            elif op=='-n':
                n=ar
            elif op=='-m':
                m=ar
            else:
                print("Opcion invalida")
    n=float(n)
    m=float(m)
    
    if 0=='+' or o == '-' or o=='/' or o=='*':
        calc=str(n)+''+o+''+str(m)
        print(calc)

            

