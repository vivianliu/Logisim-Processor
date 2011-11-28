        addi $r0 $r0 0x10
        addi $r1 $r1 -102
        add $r2 $r0 $r1
        add $r2 $r2 $r2
        addi $r3 $r3 0x7F
overflow1: add $r3 $r3 $r3

         andi $r2 $r2 0
          addi $r2 $r2 0x81
overflow2:        add $r2 $r2 $r2
