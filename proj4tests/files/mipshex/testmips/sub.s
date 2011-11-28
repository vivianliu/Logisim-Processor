        addi $r0 $r0 0x10
        addi $r1 $r1 -102
        sub $r2 $r0 $r1
        sub $r2 $r2 $r2
        andi $r3 $r3 0
        andi $r0 $r0 0
        ori $r3 $r3 0x7F
        sub $r0 $r0 $r3
overflow:
        sub $r0 $r0 $r3