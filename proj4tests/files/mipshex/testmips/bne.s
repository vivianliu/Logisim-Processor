        addi $r0 $r0 -1
        or $r1 $r0 $r0
        ori $r3 $r3 2
        sub $r2 $r1 $r3
l6:     bne $r1 $r2 l7
notexe1: addi $r1 $r0 0
        


l7:     bne $r2 $r1 l8
notexe2: lui $r0 0xff
        ori $r0 $r0 0xff
        addi $r1 $r0 0

l8:     bne $r2 $r1 l9
        j end

l9:     addi $r2 $r1 2
        bne $r0 $r1 end
shouldexe: lui $r2 0xff
        ori $r2 $r2 0xff
        addi $r1 $r2 0
        beq $r1 $r2 end
end: j end