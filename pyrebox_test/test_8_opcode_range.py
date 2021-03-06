#-------------------------------------------------------------------------------
#
#   Copyright (C) 2017 Cisco Talos Security Intelligence and Research Group
#
#   PyREBox: Python scriptable Reverse Engineering Sandbox 
#   Author: Xabier Ugarte-Pedrero 
#   
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 2 as
#   published by the Free Software Foundation.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA 02110-1301, USA.
#   
#-------------------------------------------------------------------------------

from __future__ import print_function
import sys
import api
from ipython_shell import start_shell
from utils import ConfigurationManager as conf_m
from api import CallbackManager
from hexdump import hexdump


#Callback manager
cm = None
pyrebox_print = None

def opcode_range(cpu_index,cpu,cur_pc,next_pc):
    global cm
    pgd = api.get_running_process(cpu_index)
    pyrebox_print("Opcode range callback (%x) PGD %x cur_pc %x next_pc %x\n" % (cpu_index,pgd,cur_pc,next_pc))
    start_shell()

def clean():
    '''
    Clean up everything. At least you need to place this 
    clean() call to the callback manager, that will 
    unregister all the registered callbacks.
    '''
    global cm
    print("[*]    Cleaning module")
    cm.clean()
    print("[*]    Cleaned module")

def initialize_callbacks(module_hdl,printer):
    '''
    Initilize callbacks for this module. This function
    will be triggered whenever import_module command
    is triggered.
    '''
    global cm 
    global pyrebox_print
    #Initialize printer
    pyrebox_print = printer
    pyrebox_print("[*]    Initializing callbacks")
    cm = CallbackManager(module_hdl)
    cm.add_callback(CallbackManager.OPCODE_RANGE_CB,opcode_range,name="opcode",start_opcode=0x90,end_opcode=0x90)
    pyrebox_print("[*]    Initialized callbacks")
    pyrebox_print("[!]    Test: Open calc.exe and monitor the process")


if __name__ == "__main__":
    print("[*] Loading python module %s" % (__file__))
