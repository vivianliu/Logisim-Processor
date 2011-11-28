        lui $r0, 0x33          #2033
        ori $r0, $r0, 0x44     #3044
        lui $r1, 0x33          #2133
        ori $r1, $r1, 0x44     #3544
self:   beq $r0, $r1, self       #91FF
