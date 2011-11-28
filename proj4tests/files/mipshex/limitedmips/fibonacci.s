main:   lui $r2 0xFF
        ori $r2 $r2 0xFF
        ori $r0 $r0 6
        jal fib
        lui $r0 0
        sw $r1 0($r0)
self:   j self

fib:
        addi $r2 $r2 -3
        sw $r0 0($r2)
        sw $r1 1($r2)
        sw $r3 2($r2)
        lui $r3 0
        beq $r0 $r3 returnZero
        ori $r3 $r3 1
        beq $r0 $r3 returnOne
        addi $r0 $r0 -1
        jal fib
        sw $r1 1($r2)
        lw $r0 0($r2)
        addi $r0 $r0 -2
        jal fib
        lw $r0 1($r2) # load old return value
        add $r1 $r0 $r1
        j return

returnOne:
        lui $r1 0
        ori $r1 $r1 1
        j return

returnZero:
        lui $r1 0

return:
        lw $r0 0($r2)
        lw $r3 2($r2)
        addi $r2 $r2 3
        jr $r3