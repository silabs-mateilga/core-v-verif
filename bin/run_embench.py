#!/usr/bin/env python3

################################################################################
#
# Copyright 2020 OpenHW Group
# 
# Licensed under the Solderpad Hardware Licence, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://solderpad.org/licenses/
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier:Apache-2.0 WITH SHL-2.0
# 
################################################################################
#
# run_embench : python script to fetch, set up, build and run EMBench 
#               benchmarking suite on the present cores
#
# Author: Marton Teilgård
#  email: mateilga@silabs.com
#
# Written with Python 3.5.1 on RHEL 7.7.  Your python mileage may vary.
#
# Restriction:
#
#
# TODO:
################################################################################

import argparse
import logging
import os
import sys
import subprocess



def main():

  parser = build_parser()
  args = parser.parse_args()
  paths = build_paths(args.core)

  #logging.basicConfig(filename='run_embench.log', level=logging.INFO)
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)


  if args.core == 'notset':
    print('Must specify a core to benchmark')
    sys.exit(1)



  print("Hello from the EMBench")
  print("Benchmarking core: " + args.core)

  ## clone EMBench from git
  # https://github.com/embench/embench-iot.git

  if not os.path.exists(paths['embench']):
    try:
      subprocess.run(
        ['git', 'clone', 'https://github.com/embench/embench-iot.git', 'embench'],
        cwd=paths['vlib']
      )
    except:
      logger.fatal('Git clone of EMBench failed')
    
    ## copy core-native config
    try:
      subprocess.run(
        ['cp', '-R', paths['emcfg'], 'config/corev32'],
        cwd=paths['embench']
      )
    except:
      logger.fatal('EMBench config copy failed')

    ## copy source files from bsp
    ## TODO: figure out if this can be included rather than copied
    try: 
      subprocess.run(
        ['cp ' + paths['bsp'] + '/{*.S,*.c} config/corev32/boards/corev32'],
        shell=True,
        cwd=paths['embench']
      )
    except:
      logger.fatal('EMBench bsp copy failed')
  else:
    logger.info('EMBench already checked out')


  ## build EMBench library
  try: 
    subprocess.run(
      ['build_all.py', '--arch=corev32', '--board=corev32', '--chip='+args.core, '--ldflags=-T' + paths['bsp'] + '/link.ld'],
      cwd=paths['embench']
    )
  except:
    logger.fatal('EMBench build failed')



###############################################################################
# End of Main  

def build_parser():
  """Build a parser for all the arguments"""
  parser = argparse.ArgumentParser(description='Clone and run EMBench')

  parser.add_argument(
    '-c',
    '--core',
    default='notset',
    help='Core to benchmark'
  )

  return parser

def build_paths(core):
  """map out necessary paths"""
  paths = dict()
  paths['cver'] = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
  paths['core'] = paths['cver'] + '/' + core
  paths['vlib'] = paths['core'] + '/vendor_lib'
  paths['embench'] = paths['vlib'] + '/embench'
  paths['emcfg'] = paths['cver'] + '/bin/lib/embench_cfg/corev32'
  paths['bsp'] = paths['core'] + '/bsp'

  return paths


#run main
if __name__ == '__main__':
    sys.exit(main())
