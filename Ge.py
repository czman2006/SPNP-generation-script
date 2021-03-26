import os
import sys
import string
import datetime
import math 
import fileinput
import time
import operator
#N is the number of platforms

def create(N, delay_rate, attack_rate, wait_rate, exec_rate, migration_rate, exec_times):
    file = open("mdp.c", 'w+')
    file.write('#include <stdio.h>')
    file.write('\n')
    file.write('#include "user.h"')
    file.write('\n'*3)
    file.write('/* global variable */')
    file.write('\n')
    buff = "double delay_rate = %s;\n" % (delay_rate)
    file.write(buff)
    buff = "double attack_rate = %s;\n" % (attack_rate)
    file.write(buff)
    buff = "double wait_rate = %s;\n" % (wait_rate)
    file.write(buff)
    buff = "double exec_rate = %s;\n" % (exec_rate)
    file.write(buff)
    buff = "double migration_rate = %s;\n" % (migration_rate)
    file.write(buff)
    buff = "double exec_times = %s;\n" % (exec_times)
    file.write(buff)
    file.write('\n'*3)
    file.write('/* Prototype for the function(s) */')
    file.write('\n')
    i = 1
    while i <= N:
        buff = "int guardtD%s ();\n" % (i)
        file.write(buff)
        i += 1
    i = 1
    while i <= N:
        buff = "int guardtJF%s ();\n" % (i)
        file.write(buff)
        i += 1
    file.write('int guardTstart ();\n')
    file.write('int guardTend ();\n')
    file.write('int guardDone ();\n')
    file.write('int guardjump ();\n')
    file.write('int myhalt ();\n')
    file.write('\n'*2)
    file.write('/* ================ OPTIONS ================= */\n')
    file.write('void options() {\n')
    file.write('\n')
    file.write('}\n')
    file.write('\n')
    file.write('/* ========= DEFINITION OF THE NET ========= */\n')
    file.write('void net() {\n')
    file.write('  /*  ======  PLACE  ======  */\n')
    file.write('  place("PDelay");\n')
    file.write('  init("PDelay",1);\n')
    file.write('  place("PAttack");\n')

    i = 1
    while i <= N:
        buff = '  place("PA%s");\n' % (i)
        file.write(buff)
        i += 1

    i = 1
    while i <= N:
        buff = '  place("PS%s");\n' % (i)
        file.write(buff)
        i += 1

    file.write('  place("PJob");\n')
    file.write('  init("PJob",1);\n')

    i = 1
    while i <= N:
        buff = '  place("PJ%s");\n' % (i)
        file.write(buff)
        i += 1
    
    i = 1
    while i <= N:
        buff = '  place("PJS%s");\n' % (i)
        file.write(buff)
        i += 1

    i = 1
    while i <= N:
        buff = '  place("PJF%s");\n' % (i)
        file.write(buff)
        i += 1

    i = 1
    while i <= N:
        buff = '  place("PJM%s");\n' % (i)
        file.write(buff)
        i += 1

    file.write('  place("PJStart");\n')
    buff = '  init("PJStart",%s);\n' % (exec_times)
    file.write(buff)

    file.write('  place("PTime");\n')
    file.write('  place("PJFinish");\n')
#     file.write('  place("PJEnd");\n')
    file.write('\n')
    file.write('  /*  ======  TRANSITION  ======  */\n')
    file.write('  /* Immediate Transition */\n')

    i = 1
    while i <= N:
        buff = '  imm("tA%s");\n' % (i)
        file.write(buff)
        buff = '  priority("tA%s",1);\n' % (i)
        file.write(buff)
        buff = '  probval("tA%s",1);\n' % (i)
        file.write(buff)
        i += 1
    
    i = 1
    while i <= N:
        buff = '  imm("tD%s");\n' % (i)
        file.write(buff)
        buff = '  guard("tD%s",guardtD%s);\n' % (i, i)
        file.write(buff)
        buff = '  priority("tD%s",1);\n' % (i)
        file.write(buff)
        buff = '  probval("tD%s",1);\n' % (i)
        file.write(buff)
        i += 1

    i = 1
    while i <= N:
        buff = '  imm("tJ%s");\n' % (i)
        file.write(buff)
        buff = '  priority("tJ%s",1);\n' % (i)
        file.write(buff)
        buff = '  probval("tJ%s",1);\n' % (i)
        file.write(buff)
        i += 1
    
    i = 1
    while i <= N:
        buff = '  imm("tJF%s");\n' % (i)
        file.write(buff)
        buff = '  guard("tJF%s", guardtJF%s);\n' % (i, i)
        file.write(buff)
        buff = '  priority("tJF%s",1);\n' % (i)
        file.write(buff)
        buff = '  probval("tJF%s",1);\n' % (i)
        file.write(buff)
        i += 1

    i = 1
    while i <= N:
        j = 1
        while j <= N:
            if i != j:
                buff = '  imm("t%sto%s");\n' % (i,j)
                file.write(buff)
                buff = '  guard("t%sto%s",guardjump);\n' % (i,j)
                file.write(buff)
                buff = '  priority("t%sto%s",1);\n' % (i,j)
                file.write(buff)
                buff = '  probval("t%sto%s",1);\n' % (i,j)
                file.write(buff)
            j+=1
        i+=1
    
    file.write('  imm("tFinish");\n')
    file.write('  guard("tFinish",guardDone);\n')
    file.write('  priority("tFinish",1);\n')
    file.write('  probval("tFinish",1);\n')

    file.write('  imm("t0");\n')
    file.write('  guard("t0",guardTstart);\n')
    file.write('  priority("t0",1);\n')
    file.write('  probval("t0",1);\n')

    file.write('  imm("t1");\n')
    file.write('  guard("t1",guardTend);\n')
    file.write('  priority("t1",1);\n')
    file.write('  probval("t1",1);\n')

#    file.write('  imm("tJM");\n')
#    file.write('  guard("tJM",guard1);\n')
#    file.write('  priority("tJM",1);\n')
#    file.write('  probval("tJM",1);\n')

    file.write('  /* Timed Transition */\n')
    file.write('  rateval("TDelay",delay_rate);\n')
    
    i = 1
    while i <= N:
        buff = '  rateval("TA%s",attack_rate);\n' % (i)
        file.write(buff)
        i += 1
    file.write('\n')
    i = 1
    while i <= N:
        buff = '  rateval("TMax%s",wait_rate);\n' % (i)
        file.write(buff)
        i += 1
    file.write('\n')
    i = 1
    while i <= N:
        buff = '  rateval("TJS%s",exec_rate);\n' % (i)
        file.write(buff)
        i += 1
    file.write('\n')
    i = 1
    while i <= N:
        buff = '  rateval("TJSM%s",migration_rate);\n' % (i)
        file.write(buff)
        i += 1
    file.write('\n')
    i = 1
    while i <= N:
        buff = '  rateval("TJFM%s",migration_rate);\n' % (i)
        file.write(buff)
        i += 1
    file.write('\n')
    file.write('  halting_condition(myhalt);\n')
    file.write('  /*  ======  ARC  ====== */\n')
    file.write('  /* Input Arcs */\n')
    file.write('  iarc("TDelay","PDelay");\n')
    file.write('  iarc("tFinish","PJStart");\n')
#    file.write('  iarc("tJM","PJFinish");\n')
    file.write('  iarc("t0","PJStart");\n')
    file.write('  iarc("t1","PTime");\n')

    i = 1
    while i <= N:
        buff = '  iarc("tA%s","PAttack");\n' % (i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  iarc("TA%s","PA%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  iarc("TMax%s","PS%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  iarc("tD%s","PS%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')
    
    i = 1
    while i <= N:
        buff = '  iarc("tJ%s","PJob");\n' % (i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  iarc("TJS%s","PJ%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  iarc("tJF%s","PJ%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  iarc("TJSM%s","PJS%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  iarc("TJFM%s","PJF%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        j = 1
        while j <= N:
            if i != j:
                buff = '  iarc("t%sto%s","PJM%s");\n' % (i,j,i)
                file.write(buff)
            j+=1
        i+=1
    file.write('\n')
    
    file.write('  /* Output Arcs */\n')
    file.write('  oarc("TDelay","PAttack");\n')
    file.write('  oarc("tFinish","PJFinish");\n')
#    file.write('  oarc("tJM","PJEnd");\n')
    file.write('  oarc("t0","PTime");\n')
    file.write('  oarc("t1","PJStart");\n')

    i = 1
    while i <= N:
        buff = '  oarc("tA%s","PA%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  oarc("TA%s","PS%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  oarc("tD%s","PAttack");\n' % (i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  oarc("TMax%s","PAttack");\n' % (i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  oarc("tJ%s","PJ%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        buff = '  oarc("TJS%s","PJS%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')
    
    i = 1
    while i <= N:
        buff = '  oarc("TJSM%s","PJM%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')
    
    i = 1
    while i <= N:
        buff = '  oarc("tJF%s","PJF%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')
    
    i = 1
    while i <= N:
        buff = '  oarc("TJFM%s","PJM%s");\n' % (i, i)
        file.write(buff)
        i += 1     
    file.write('\n')

    i = 1
    while i <= N:
        j = 1
        while j <= N:
            if i != j:
                buff = "  oarc(\"t%sto%s\",\"PJ%s\");\n" % (i,j,j)
                file.write(buff)
            j+=1
        i+=1
    file.write('}')
    file.write('\n')
    
    file.write('/* GUARD Functions */\n')
    i = 1
    while i <= N:
        buff = 'int guardtD%s () { \n' % (i)
        file.write(buff)
        buff = 'if (mark("PJ%s")==1) return 1;\n' % (i)
        file.write(buff)
        file.write('else return 0;\n')
        file.write('}\n')
        i += 1

    i = 1
    while i <= N:
        buff = 'int guardtJF%s () { \n' % (i)
        file.write(buff)
        buff = 'if (mark("PS%s")==1) return 1;\n' % (i)
        file.write(buff)
        file.write('else return 0;\n')
        file.write('}\n')
        i += 1

    file.write('int guardDone () {\n')
    file.write('if (')
    i = 1
    while i < N:
        buff = '(mark("PJS%s")==1) || ' % (i)
        file.write(buff)
        i += 1        
    buff = '(mark("PJS%s")==1)) return 1;\n' % (N)
    file.write(buff)
    file.write('else return 0;\n')
    file.write('}\n')

    file.write('int guardTstart() {\n')
    file.write('if (')
    i = 1
    while i < N:
        buff = '(mark("PJF%s")==1) || ' % (i)
        file.write(buff)
        i += 1        
    buff = '(mark("PJF%s")==1)) return 1;\n' % (N)
    file.write(buff)
    file.write('else return 0;\n')
    file.write('}\n')

    file.write('int guardTend() {\n')
    file.write('if (')
    i = 1
    while i < N:
        buff = '(mark("PJM%s")==1) || ' % (i)
        file.write(buff)
        i += 1        
    buff = '(mark("PJM%s")==1)) return 1;\n' % (N)
    file.write(buff)
    file.write('else return 0;\n')
    file.write('}\n')

    file.write('int guardjump () {\n')
    file.write('if (mark("PJFinish")==1) return 0;\n')
    file.write('else return 1;\n')
    file.write('}\n')

    file.write('/* HALTING Functions */\n')

    file.write('int myhalt () {\n')
    buff = 'if (mark("PJFinish")==%s) return 0;\n' % (exec_times)
    file.write(buff)
    file.write('else return 1;\n')
    file.write('}\n')
    
    file.write('/* ======= DEFINITION OF THE FUNCTIONS ====== */')
    file.write('\n')
    file.write('int assert() { ')
    file.write('\n')
    file.write('} ')
    file.write('\n')
    file.write('void ac_init() { ')
    file.write('\n')
    file.write('/* Information on the net structure */ ')
    file.write('\n')
    file.write('pr_net_info();')
    file.write('\n')
    file.write('} ')
    file.write('\n')
    file.write('\n')
    file.write('void ac_reach() { ')
    file.write('\n')
    file.write('/* Information on the reachability graph */ ')
    file.write('\n')
    file.write('pr_rg_info();')
    file.write('\n')
    file.write('\n')
    file.write('} ')
    file.write('\n')    
    file.write('\n')

    buff = 'double outFun0() { \n'
    file.write(buff)
    buff = '  return('
    file.write(buff)
    i = 1
    while i < N:
        buff = 'rate("TJFM%s")+' % (i)
        file.write(buff)
        i += 1
    buff = 'rate("TJFM%s"));\n' % (N)
    file.write(buff)
    file.write('}\n')

    buff = 'double outFun1() { \n'
    file.write(buff)
    buff = '  return('
    file.write(buff)
    i = 1
    while i < N:
        buff = 'rate("TJS%s")+' % (i)
        file.write(buff)
        i += 1
    buff = 'rate("TJS%s"));\n' % (N)
    file.write(buff)
    file.write('}\n')

    buff = 'double outFun2() { \n'
    file.write(buff)
    buff = '  return('
    file.write(buff)
    i = 1
    while i < N:
        buff = 'rate("TA%s")+' % (i)
        file.write(buff)
        i += 1
    buff = 'rate("TA%s"));\n' % (N)
    file.write(buff)
    file.write('}\n')

    file.write('void ac_final() { ')
    file.write('\n')
    file.write('int loop;\n')
    file.write('solve(100.0);\n')
    file.write('pr_cum_expected("fail times", outFun0);\n')
    file.write('pr_cum_expected("success times", outFun1);\n')
    file.write('pr_cum_expected("attack times", outFun2);\n')
    file.write('solve(1);\n')
    file.write('pr_mtta("test");\n')
    file.write('}\n')


N = 3
delay_rate = 1.0
attack_rate = 0.3333
wait_rate = 5.0
exec_rate = 0.5
migration_rate = 48.0
exec_times = 1
create(N, delay_rate, attack_rate, wait_rate, exec_rate, migration_rate, exec_times) 
