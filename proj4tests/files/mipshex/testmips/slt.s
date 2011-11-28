        addi $r0 $r0 0xF0
        addi $r1 $r1 4
        sllv $r0 $r0 $r1
        addi $r1 $r1 1
        slt $r2 $r0 $r1
        slt $r3 $r1 $r0
