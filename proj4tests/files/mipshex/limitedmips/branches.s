        beq $r0 $r0 start
badness:
        lui $r0 0xFF
        beq $r0 $r0 badness
label1:
        lui $r0 3
        bne $r0 $r3 label2

start:  lui $r0 1
        beq $r0 $r1 badness
        lui $r0 2
        bne $r0 $r1 label1

label2: lui $r0 4
end:    ori $r2 $r0 0
        beq $r2 $r0 end
        ori $r2 $r0 2
