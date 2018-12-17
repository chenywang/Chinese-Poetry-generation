#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse

import os

from generate import Generator
from paths import save_dir
from plan import train_planner

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chinese poem generation.')
    parser.add_argument('-p', dest='planner', default=False,
                        action='store_true', help='train planning model')
    parser.add_argument('-g', dest='generator', default=False,
                        action='store_true', help='train generation model')
    parser.add_argument('-a', dest='all', default=False,
                        action='store_true', help='train both models')
    parser.add_argument('--clean', dest='clean', default=False,
                        action='store_true', help='delete all models')
    args = parser.parse_args()
    if args.clean:
        for f in os.listdir(save_dir):
            os.remove(os.path.join(save_dir, f))
    else:
        if args.all or args.planner:
            train_planner()
        if args.all or args.generator:
            generator = Generator()
            generator.train(n_epochs=1000)
        print("All training is done!")
