import subprocess as sp
import time
import sys
from click import command
import os
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="getopt")
    parser.add_argument("-c", "--command", type=str, required=True, 
        help="string")
    parser.add_argument("-f", "--output_file", type=str, required=True, 
        help="string")
    parser.add_argument("-l", "--log_file", type=str, required=True, 
        help="string")
    args = parser.parse_args()

    with open(args.output_file, "ab") as output_file:
        proceso = sp.Popen(args.command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        stdout, stderr = proceso.communicate()
        procesoo = sp.Popen("date", stdout=sp.PIPE, stderr=sp.PIPE)
        stdout2, stderr2 = procesoo.communicate()
        output_file.write(stdout)

    with open(args.log_file, "ab") as log_file:
        if stderr == b'':
            log_file.write(stdout2[:-1] + b': Comando ' + bytes(args.command, encoding = "utf-8") + b' ejecutado correctamente.\n')
        else:
            log_file.write(stdout2[:-1] + b' ' + stderr)