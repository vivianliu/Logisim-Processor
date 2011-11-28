#!/usr/bin/env python

"""
assembler.py: rather primitive two-pass assembler. Get the labels, then
assemble the instructions.
"""

import re
import sys
import optparse

symbols = {}

instructions = []

relocations = []

class AssemblerError(Exception):
  pass

class AssemblerSyntaxError(AssemblerError):
  def __init__(self,line,reason):
    self.line = line
    self.reason = reason
  def __str__(self):
    return "Syntax error on line %d: %s" % (self.line,self.reason)

class AssemblerRangeError(AssemblerError):
  def __init__(self,line,reason):
    self.line = line
    self.reason = reason
  def __str__(self):
    return "Range error on line %d: %s" % (self.line,self.reason)

labelre = re.compile(r"""^(?P<labels>.*:)?(?P<gunk>[^:]*)$""")
commentre = re.compile(r"""^(?P<important>[^#]*)(?P<comment>#.*)?$""")
alnumunderre = re.compile(r"""^\w+$""")

rtype_re  = re.compile(r'''^(?P<instr>(or|and|add|sub|sllv|srlv|srav|slt))\s+(?P<rd>\$r[0,1,2,3])\s+(?P<rs>\$r[0,1,2,3])\s+(?P<rt>\$r[0,1,2,3])$''')
immed_re  = re.compile(r'''^(?P<instr>(ori|addi|andi))\s+(?P<rt>\$r[0,1,2,3])\s+(?P<rs>\$r[0,1,2,3])\s+(?P<immed>-?(0x)?[0-9a-fA-F]+)$''')
lui_re    = re.compile(r'''^(?P<instr>lui)\s+(?P<rt>\$r[0,1,2,3])\s+(?P<immed>-?(0x)?[0-9a-fA-F]+)$''')
disp_re   = re.compile(r'''^(?P<instr>disp)\s+(?P<rs>\$r[0,1,2,3])\s+(?P<immed>-?(0x)?[0-9a-fA-F]+)$''')
mem_re    = re.compile(r'''^(?P<instr>(lw|sw))\s+(?P<rt>\$r[0,1,2,3])\s+(?P<immed>-?(0x)?[0-9a-fA-F]+)\s*\(\s*(?P<rs>\$r[0,1,2,3])\s*\)$''')
j_re      = re.compile(r'''^(?P<instr>(j|jal))\s+(?P<label>\w+)$''')
la_re     = re.compile(r'''^(?P<instr>(la))\s+(?P<rt>\$r[0,1,2,3])\s+(?P<label>\w+)$''')
li_re     = re.compile(r'''^(?P<instr>(li))\s+(?P<rt>\$r[0,1,2,3])\s+(?P<immed>-?(0x)?[0-9a-fA-F]+)$''')
branch_re = re.compile(r'''^(?P<instr>(beq|bne))\s+(?P<rs>\$r[0,1,2,3])\s+(?P<rt>\$r[0,1,2,3])\s+(?P<label>\w+)$''') #note switch
jr_re     = re.compile(r'''^(?P<instr>(jr))\s+(?P<rs>\$r[0,1,2,3])$''')

opcodes = {
  'disp':1,
  'lui':2,
  'ori':3,
  'addi':4,
  'andi':5,
  'jal':6,
  'j':7,
  'jr':8,
  'beq':9,
  'bne':10,
  'lw':11,
  'sw':12,
}

functs = {
  'or':0,
  'and':1,
  'add':2,
  'sub':3,
  'sllv':4,
  'srlv':5,
  'srav':6,
  'slt':7,
}
def isPseudoInstruction(s):
  return la_re.match(s) or li_re.match(s)

def validLabel(s):
  return alnumunderre.match(s) != None

def fill_symbol_table(inputFile):
  lineNo = 1
  instructionsSeen = 0
  for line in inputFile:
    #strip any comments
    match = commentre.match(line)
    
    if not match:
      raise AssemblerSyntaxError(lineNo,"Unable to parse line: %s" % line)
    
    line = match.group('important')
    
    line = line.strip()
    
    match = labelre.match(line)
    
    if not match:
      raise AssemblerSyntaxError(lineNo,"Unable to parse line: %s" % line)
    
    labels_string = match.group('labels')
    
    if labels_string:
      labels = labels_string[:-1].split(':')
    else:
      labels = []
    
    for label in labels:
      if not validLabel(label):
        raise AssemblerSyntaxError(lineNo,"Invalid label: '%s'"%label)
      if label in symbols:
        raise AssemblerSyntaxError(lineNo,"Label %s already defined" % label)
      symbols[label] = instructionsSeen
    
    instruction = match.group('gunk').replace(',',' ').strip()
    if len(instruction) != 0:
      #there's an instruction here, so increment the number of instructions
      #if we had any pseudoinstructions, we'd do analysis and increment by
      #more than one here
      instructionsSeen += 1
      if isPseudoInstruction(instruction): #currently all pseudoinstructions have length 2
        instructionsSeen += 1
    lineNo+=1

def assemble_instructions(inputFile):
  lineNo = 1
  instructionsSeen = 0
  instructions = []
  for line in inputFile:
    #strip any comments
    match = commentre.match(line)
    assert(match)
    line = match.group('important')
    
    line = line.strip()
    
    match = labelre.match(line)
    
    instruction = match.group('gunk').replace(',',' ').strip()
    
    rtype    = rtype_re.match(instruction)
    immed    = immed_re.match(instruction)
    lui      = lui_re.match(instruction)
    disp     = disp_re.match(instruction)
    mem      = mem_re.match(instruction)
    j        = j_re.match(instruction)
    la       = la_re.match(instruction)
    li       = li_re.match(instruction)
    branch   = branch_re.match(instruction)
    jr       = jr_re.match(instruction)
    
    if len(instruction) != 0:
      num = 0
      if rtype:
        rs = int(rtype.group('rs')[2])
        rt = int(rtype.group('rt')[2])
        rd = int(rtype.group('rd')[2])
        funct = functs[rtype.group('instr')]
        num = 0 << 12 | rs << 10 | rt << 8 | rd << 6 | funct
        debug("instruction: %s rtype: rs: %d rt: %d rd: %d funct:%d num: %04x" % (instruction,rs,rt,rd,funct,num))
      elif immed:
        rs = int(immed.group('rs')[2])
        rt = int(immed.group('rt')[2])
        opcode = opcodes[immed.group('instr')]
        immediate = int(immed.group('immed'),0)
        if immediate > 2 ** 8:
          raise AssemblerSyntaxError(lineNo,"immediate too big")
        num = opcode << 12 | rs << 10 | rt << 8 | (immediate & 255)
        debug("instruction: %s rs: %d rt: %d opcode: %d immediate: %d num: %04x" % (instruction,rs,rt,opcode,immediate,num))
      elif lui:
        rt = int(lui.group('rt')[2])
        opcode = opcodes[lui.group('instr')]
        immediate = int(lui.group('immed'),0)
        if immediate > 2 ** 8:
          raise AssemblerSyntaxError(lineNo,"immediate too big")
        num = opcode << 12 | 0 << 10 | rt << 8 | (immediate & 255)
        debug("instruction: %s rt: %d opcode: %d immediate: %d num: %04x" % (instruction,rt,opcode,immediate,num))
      elif disp:
        rs = int(disp.group('rs')[2])
        opcode = opcodes[disp.group('instr')]
        immediate = int(disp.group('immed'),0)
        if immediate > 2 ** 8:
          raise AssemblerSyntaxError(lineNo,"immediate too big")
        num = opcode << 12 | rs << 10 | 0 << 8 | (immediate & 255)
        debug("instruction: %s rs: %d opcode: %d immediate: %d num: %04x" % (instruction,rs,opcode,immediate,num))
      elif mem:
        opcode = opcodes[mem.group('instr')]
        rs = int(mem.group('rs')[2])
        rt = int(mem.group('rt')[2])
        immediate = int(mem.group('immed'),0)
        if immediate > 2 ** 8:
          raise AssemblerSyntaxError(lineNo,"immediate too big")
        num = opcode << 12 | rs << 10 | rt << 8 | (immediate & 255)
        debug("instruction: %s rs: %d rt: %d opcode: %d immediate: %d num: %04x" % (instruction,rs,rt,opcode,immediate,num))
      elif la: #pseudoinstruction, does lui followed by ori
        rt = int(la.group('rt')[2])       
        #find label 
        label = la.group('label')
        if label not in symbols:
          raise AssemblerSyntaxError(lineNo,"unknown label %s" % la.group('label'))
        instructionNo = symbols[label] #needs to be broken into lows and highs
        highs = (instructionNo >> 8) & 255
        lows = instructionNo & 255
        opcode = opcodes['lui']
        num1 = opcode << 12 | 0 << 10 | rt << 8 | highs
        instructionsSeen += 1 # additional increment, since this is a pseudoinstruction
        instructions.append(num1)
        opcode = opcodes['ori']
        num = opcode << 12 | rt << 10 | rt << 8 | lows
        debug("pseudoinstruction: %s rt: %d addr: %d num1: %04x num2: %04x" % (instruction,rt,instructionNo & 4095,num1,num))
      elif li: #pseudoinstruction, does lui followed by ori
        rt = int(li.group('rt')[2])       
        immediate = int(li.group('immed'),0)
        if immediate > 2 ** 16:
          raise AssemblerSyntaxError(lineNo,"li: immediate too big")
        highs = (immediate >> 8) & 255
        lows = immediate & 255
        opcode = opcodes['lui']
        num1 = opcode << 12 | 0 << 10 | rt << 8 | highs
        instructionsSeen += 1 # additional increment, since this is a pseudoinstruction
        instructions.append(num1)
        opcode = opcodes['ori']
        num = opcode << 12 | rt << 10 | rt << 8 | lows
        debug("pseudoinstruction: %s rt: %d immediate: %d num1: %04x num2: %04x" % (instruction,rt,immediate,num1,num))
      elif j:
        opcode = opcodes[j.group('instr')]
        #find label
        label = j.group('label')
        if label not in symbols:
          raise AssemblerSyntaxError(lineNo,"unknown label %s" % j.group('label'))
        instructionNo = symbols[label]
        thisInstruction = instructionsSeen
        if thisInstruction & 0xF000 != instructionNo & 0xF000:
          raise AssemblerRangeError(lineNo,"label %s is in another jump zone (instr: %04x, target:%04x)" % (label,thisInstruction,instructionNo))
        num = opcode << 12 | (instructionNo & 4095)
        debug("instruction: %s addr: %d num: %04x" % (instruction,instructionNo & 4095,num))
      elif branch:
        rs = int(branch.group('rs')[2])
        rt = int(branch.group('rt')[2])
        opcode = opcodes[branch.group('instr')]
        #find label
        label = branch.group('label')
        if label not in symbols:
          raise AssemblerSyntaxError(lineNo,"unknown label %s" % branch.group('label'))
        instructionNo = symbols[label]
        offset = instructionNo - (instructionsSeen + 1)
        if offset > 2 ** 8:
          raise AssemblerRangeError(lineNo,"label %s is too far away: %d instructions from pc+1" % (label,offset))
        num = opcode << 12 | rs << 10 | rt << 8 | (offset & 255)
        debug("instruction: %s rs: %d rt: %d opcode: %d offset: %d num: %04x" % (instruction,rs,rt,opcode,offset,num))
      elif jr:
        rs = int(jr.group('rs')[2])
        opcode = opcodes[jr.group('instr')]
        num = opcode << 12 | rs << 10
        debug("instruction: %s rs: %d num: %04x" % (instruction,rs,num))
      else:
        raise AssemblerSyntaxError(lineNo,"Can't parse instruction '%s'" % instruction)
      #there's an instruction here, so increment the number of instructions
      #if we had any pseudoinstructions, we'd do analysis and increment by
      #more than one here
      instructionsSeen += 1
      instructions.append(num)
    lineNo+=1
  return instructions

def print_instructions(instructions,outfile):
  print >> outfile, "v2.0 raw"
  for instruction in instructions:
    print >> outfile, "%04x" % instruction

verbose = False

def debug(*args):
  if verbose:
    sys.stdout.write(' '.join([str(arg) for arg in args]) + '\n')

if __name__ == "__main__":
  usage = "%prog infile [options]"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option('-o','--out',dest='output_file',type='string',
                    default='a.hex',help="Specify output filename")
  parser.add_option('-v','--verbose',dest='verbose',
                    action='store_true',default=False, help='verbose debug mode')
  options,args = parser.parse_args()
  if len(args) != 1:
    parser.error("Incorrect command line arguments")
    sys.exit(1)
  
  verbose = options.verbose
  
  output_file = options.output_file
  input_file = args[0]
  if re.match(r""".*(?P<extension>\.s)$""",input_file,re.I) and output_file == 'a.hex':
    output_file = input_file[:-1] + "hex"
  
  try:
    infile = open(input_file)
  except IOError,e:
    print >> sys.stderr, "Unable to open input file %s" % input_file
    sys.exit(1)
  try:
    fill_symbol_table(infile)
    infile.seek(0)
    instructions = assemble_instructions(infile)
    infile.close()
  except AssemblerError, e:
    print >> sys.stderr, str(e)
    sys.exit(1)
  try:
    outfile = open(output_file,'w')
    print_instructions(instructions,outfile)
    outfile.close()
  except IOError,e:
    print >> sys.stderr, "Unable to write to output file %s" % output_file
    sys.exit(1)
  sys.exit(0)
