        addi $r0 $r0 -1
        or $r1 $r0 $r0
        ori $r3 $r3 2
        sub $r2 $r1 $r3
l1:     beq $r0 $r1 l2 #I deliberately call consecutive beq
l2:     beq $r0 $r1 l3
        j end
l3:     beq $r0 $r1 l4
        j end
l4:     andi $r0 $r0 0
        beq $r0 $r1 l5

shouldexe:   addi $r0 $r0 -1
        or $r1 $r0 $r0
        addi $r2 $r1 -2
l5:     or $r0 $r0 $r0
        beq $r1 $r2 end
end: j end