        addi $r0 $r0 0x1
        addi $r1 $r1 0x10
        and $r2 $r0 $r1
        and $r3 $r1 $r2
        and $r3 $r2 $r3
        addi $r3 $r3 232
        and $r2 $r2 $r3