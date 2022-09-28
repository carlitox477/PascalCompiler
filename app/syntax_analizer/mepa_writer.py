from io import TextIOWrapper
# PROGRAM: instructions available
# HEAP: data to bi managed by MEPA instructions
# DISPLAY: pointers to HEAP region 
# i: Next instruction to be executed
# TOP: HEAP top
# LABEL_HASHMAP = Hashmap which allow us to look for an instruction based in a label name

class MepaWriter:
    
    def __init__(self, file: TextIOWrapper) -> None:
        self.top_write_pointer=0
        self.file = file
        pass

    def close_file(self) -> None:
        self.file.close()
        pass

    # Artihmetical operations
    def add(self):
        """
            Write SUMA.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] + HEAP[TOP ]
                2. TOP = TOP - 1
        """
        self.file.write("ADD\n")
        pass

    def sub(self):
        """
            Write SUST.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] - HEAP[TOP ]
                2. TOP = TOP - 1
        """
        self.file.write("SUST\n")
        pass

    def mul(self):
        """
            Write MULT.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] * HEAP[TOP ]
                2. TOP = TOP - 1
        """
        self.file.write("MULT\n")
        pass

    def div(self):
        """
            Write DIVI.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] / HEAP[TOP ]
                2. TOP = TOP - 1
        """
        self.file.write("DIVI\n")
        pass

    def mod(self):
        """
            Write MODU.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] MOD HEAP[TOP ]
                2. TOP = TOP - 1
        """
        self.file.write("MODU\n")
        pass

    def uminus(self):
        """
            Write UMEN.
            Do:

                1. HEAP[TOP] = -HEAP[TOP]
        """
        self.file.write("UMEN\n")
        pass

    # Logical operations
    def _and(self):
        """
            Write CONJ.
            Do:

                1. IF HEAP[TOP - 1] = 1 AND HEAP[TOP] = 1 THEN HEAP[TOP - 1] = 1; ELSE HEAP[TOP - 1] = 0 
                2. TOP = TOP - 1
        """
        self.file.write("CONJ\n")
        pass

    def _or(self):
        """
            Write DISJ.
            Do:

                1. IF HEAP[TOP - 1] = 1 or HEAP[TOP] = 1 THEN HEAP[TOP - 1] = 1; ELSE HEAP[TOP - 1] = 0 
                2. TOP = TOP - 1
        """
        self.file.write("DISJ\n")
        pass

    def _not(self):
        """
            Write NEGA.
            Do:

                1. IF HEAP[TOP] = HEAP[TOP] - 1
        """
        self.file.write("NEGA\n")
        pass
    
    # Comparisson operations
    def lt(self):
        """
            Write CMME.
            Do:

                1. IF HEAP[TOP - 1] < HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        self.file.write("CMME\n")
        pass

    def gt(self):
        """
            Write CMMA.
            Do:

                1. IF HEAP[TOP - 1] > HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        self.file.write("CMMA\n")
        pass

    def eq(self):
        """
            Write CMIG.
            Do:

                1. IF HEAP[TOP - 1] = HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        self.file.write("CMIG\n")
        pass

    def neq(self):
        """
            Write CMDG.
            Do:

                1. IF HEAP[TOP - 1] <> HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        self.file.write("CMDG\n")
        pass

    def leq(self):
        """
            Write CMNI.
            Do:

                1. IF HEAP[TOP - 1] <= HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        self.file.write("CMNI\n")
        pass

    def gte(self):
        """
            Write CMYI.
            Do:

                1. IF HEAP[TOP - 1] >= HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        self.file.write("CMYI\n")
        pass

    # Jump instructions
    def jmp(self, label:str ):
        """
            Write DSVS label.
            Do:
                
                1. i = LABEL_HASHMAP[label]
        """
        self.file.write(f"DSVS {label}\n")
        pass
    
    def jz(self, label:str ):
        """
            Write DSVF label.
            Do:
                
                1. IF HEAP[TOP] = 0 THEN i = LABEL_HASHMAP[label] ELSE i = i + 1
                2. TOP = TOP - 1
        """
        self.file.write(f"DSVF {label}\n")
        pass

    def nop(self, label:str ):
        """
            Write label NADA.
            Do:
                1. LABEL_HASHMAP[label] = i - 1 
        """
        self.file.write(f"{label} NADA\n")
        pass
    
    # Read/write instruction
    def read(self):
        """
            Write LEER.
            Do:
                1. TOP = TOP + 1
                2. HEAP[TOP] = input sent by stream
        """
        self.file.write(f"LEER\n")
        pass

    def write(self):
        """
            Write IMPR
            Do:

                1. print HEAP[TOP]
                2. TOP = TOP - 1
        """
        self.file.write(f"IMPR\n")
        pass

    # Push instructions
    def push_c(self, constant_value:str ):
        """
            Write APCT constant_value.
            Do:
        
                1. TOP = TOP + 1
                1. HEAP[TOP] = constant_value
        """
        self.file.write(f"APCT {constant_value}\n")
        pass
    
    def push_v(self, scope_level: int ,variable_offset: int ):
        """
            Write APVL scope_level, variable_offset.
            Do:
                
                1. TOP = TOP + 1
                2. HEAP[TOP] = HEAP[DISPLAY[scope_level] + variable_offset ]
        """
        self.file.write(f"APVL {scope_level}, {variable_offset}\n")
        pass
    
    # Store
    def store(self, scope_level: int ,variable_offset: int ):
        """
            Write ALVL scope_level, variable_offset.
            Do:
                
                1. HEAP[DISPLAY[scope_level] + variable_offset ] = HEAP[TOP]
                2. TOP = TOP - 1
        """
        self.file.write(f"ALVL {scope_level}, {variable_offset}\n")
        pass
    
    # Programs and procedures
    def init(self):
        """
            Write INPP.
            Do:
                
                1. TOP = - 1
                2. DISPLAY[0] = 0
        """
        self.file.write("INPP\n")
        pass
    
    def enter(self, procedure_level: int):
        """
            Write ENPR procedure_level.
            Do:
                
                1. TOP = TOP + 1
                2. HEAP[TOP] = DISPLAY[procedure_level]
                3. DISPLAY[procedure_level] = TOP + 1
        """
        self.file.write(f"ENPR {procedure_level}\n")
        pass
    
    def call(self, procedure_label: int):
        """
            Write LLPR procedure_level.
            Do:
                
                1. TOP = TOP + 1
                2. HEAP[TOP] = i + 1
                3. i = LABEL_HASHMAP[procedure_label]
        """
        self.file.write(f"LLPR {procedure_label}\n")
        pass
    
    def malloc(self, memory_to_alloc: int):
        """
            Write RMEM memory_to_alloc.
            Do:
                
                1. TOP = TOP + memory_to_alloc
                
        """
        self.file.write(f"RMEM {memory_to_alloc}\n")
        pass
    
    def free(self, memory_to_free: int):
        """
            Write LMEM memory_to_free.
            Do:
                
                1. TOP = TOP - memory_to_free
        """
        self.file.write(f"LMEM {memory_to_free}\n")
        pass
    
    def _return(self, procedure_level: int, memory_required_by_parameters: int):
        """
            Write RTPR procedure_level, memory_required_by_parameters.
            Do:
                
                1. DISPLAY[procedure_level] = HEAP[TOP]
                2. i = HEAP[TOP - 1]
                1. TOP = TOP - (memory_required_by_parameters + 2)
        """
        self.file.write(f"RTPR {procedure_level}, {memory_required_by_parameters}\n")
        pass
    
    def halt(self):
        """
            Write PARA.
        """
        self.file.write("PARA\n")
        pass

    pass