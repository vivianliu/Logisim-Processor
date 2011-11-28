        lui $r0 0xF0
        ori $r0 $r0 0xF0
        lui $r1 0
        ori $r1 $r1 5
        slt $r2 $r0 $r1
        lui $r0 0x7F
        ori $r0 $r0 0x0F
        slt $r2 $r0 $r1
