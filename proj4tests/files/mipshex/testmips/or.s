        addi $r0 $r0 0x1
        addi $r1 $r0 0x10
        or $r2 $r0 $r1
        or $r3 $r1 $r2
        or $r3 $r2 $r3
        addi $r3 $r3 1
        or $r2 $r2 $r3