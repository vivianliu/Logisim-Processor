main:   lui $r1 0xff
        ori $r1 $r1 0x53
        andi $r1 $r1 0x9
        ori $r3 $r0 17
        j j6
j1:     addi $r0 $r0 5
        addi $r1 $r1 0xaa
        srlv $r2 $r1 $r0
        addi $r0 $r0 10
        j j2
j2:     j j4
j3:     j j1
j4:     j j8
j5:     j end
j6:     j j3
j7:     j j5
j8:     j j7
end:    disp $r1 0