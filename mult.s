mult:
	lui $r0 0x00
	ori $r0 $r0 0x00
	lw $r1 0($r0)
	lw $r2 1($r0)
	sw $r0 2($r0)

loop:
	addi $r3 $r0 1
	slt $r3 $r2 $r3
	bne $r3 $r0 return
	lw $r3 2($r0)
	add $r3 $r3 $r1
	sw $r3 2($r0)
	addi $r2 $r2 -1
	j loop
	
return:
	j return