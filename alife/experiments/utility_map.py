#!/bin/env python2

from alife.worlds.world import World, Point
from alife.agents.agent import Agent

# common settings:
dimX=10
dimY=10
items=None

def main():
  w = World(dimX, dimY, items)

if __name__ == "__main__":
    main()
