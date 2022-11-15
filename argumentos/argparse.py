import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ejercicio2")

    parser.add_argument("-i", "--existente", type=str, required=True, 
        help="archivo existente")
    parser.add_argument("-o", "--nuevo", type=str, required=True, 
        help="archivo nuevo")
    args = parser.parse_args()

    print('Existente: %s.' % args.existente)
    print('Nuevo: %d.' % args.nuevo)

    with open(args.existente, "r") as entrada:
        with open(args.nuevo, "w") as salida:
            salida.write(entrada.read())