/* Copyright (C) 2017 Embecosm Limited and University of Bristol

   Contributor Graham Markall <graham.markall@embecosm.com>

   This file is part of Embench and was formerly part of the Bristol/Embecosm
   Embedded Benchmark Suite.

   SPDX-License-Identifier: GPL-3.0-or-later */

#include <support.h>
#include <stdint.h>
#include "boardsupport.h"

void
initialise_board ()
{
  printf("Initialize board corev32 \n");
  __asm__ volatile ("li a0, 0" : : : "memory");
}

void __attribute__ ((noinline)) __attribute__ ((externally_visible))
start_trigger ()
{
  printf("start of test \n");
  //reset cycle counter
  TICKS_ADDR = 0;
  
  __asm__ volatile ("li a0, 0" : : : "memory");
}

void __attribute__ ((noinline)) __attribute__ ((externally_visible))
stop_trigger ()
{
  uint32_t cycle_cnt = TICKS_ADDR;
  printf("end of test \n");
  printf("stopped at cycle: %d \n", cycle_cnt);
  cycle_cnt = TICKS_ADDR;
  

  _exit(0);
}
 