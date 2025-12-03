#!/usr/bin/env python3
import argparse
import sys

class RocketCli:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Rocket flight simulation",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        self.subparsers = self.parser.add_subparsers(
            dest="command",
            help="Available commands"
        )

        self.simulation_parser = self.subparsers.add_parser(
            "simulation",
            help="Simulation setup"
        )
        self.simulation_parser.add_argument(
            "--add-rocket",
            help="Add empty rocket entity"
        )

def main():


    

if __name__ == "__main__":
    main()
