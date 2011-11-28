main:   lui $r2 0xFF
        ori $r2 $r2 0xFF
        addi $r2 $r2 -1
        sw $r2 0($r2)  #store $sp onto stack haha what the heck it is
        jal normalfunc
        lw $r2 0($r2)
        addi $r2 $r2 1
        jal abnormalfunc1
        lui $r0 0
end:    j end

abnormalfunc1:  jal abnormalfunc2   #I deliberately call consecutive jal without saving $r3 onto stack.
abnormalfunc2:  jal abnormalfunc3
abnormalfunc3:  addi $r1 $r1 -102
                sub $r2 $r0 $r1
                sub $r2 $r2 $r2
                andi $r3 $r3 0
                ori $r3 $r3 8
                jr $r3

normalfunc:     addi $r2 $r2 -1
                sw $r0 0($r2)
                lui $r0 0xff
                ori $r0 $r0 0x9
                lw $r0 0($r2)
                addi $r2 $r2 1
                jr $r3