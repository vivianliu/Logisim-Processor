octal:
	lui $r0 0x00
	lw $r1 0($r0)
	lui $r2 0x01
	ori $r2 $r2 0xff
	and $r3 $r1 $r2
	disp $r3 0x00
self:
	j self