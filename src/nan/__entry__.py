import sys
import os


def main():
    os.execv(sys.executable, [sys.executable, '-m', 'nan'])
