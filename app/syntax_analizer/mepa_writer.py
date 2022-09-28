from io import TextIOWrapper
# PROGRAM: instructions available
# HEAP: data to bi managed by MEPA instructions
# DISPLAY: pointers to HEAP region 
# i: Next instruction to be executed
# TOP: HEAP top
# LABEL_HASHMAP = Hashmap which allow us to look for an instruction based in a label name

class MepaWriter:

    # Artihmetical operations
    @staticmethod
    def add(file: TextIOWrapper):
        """
            Write SUMA.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] + HEAP[TOP ]
                2. TOP = TOP - 1
        """
        file.write("ADD")
        pass

    @staticmethod
    def sub(file: TextIOWrapper):
        """
            Write SUST.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] - HEAP[TOP ]
                2. TOP = TOP - 1
        """
        file.write("SUST")
        pass

    @staticmethod
    def mul(file: TextIOWrapper):
        """
            Write MULT.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] * HEAP[TOP ]
                2. TOP = TOP - 1
        """
        file.write("MULT")
        pass

    @staticmethod
    def div(file: TextIOWrapper):
        """
            Write DIVI.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] / HEAP[TOP ]
                2. TOP = TOP - 1
        """
        file.write("ADD")
        pass

    @staticmethod
    def mod(file: TextIOWrapper):
        """
            Write MODU.
            Do:

                1. HEAP[TOP - 1] = HEAP[TOP - 1] MOD HEAP[TOP ]
                2. TOP = TOP - 1
        """
        file.write("MODU")
        pass

    @staticmethod
    def uminus(file: TextIOWrapper):
        """
            Write UMEN.
            Do:

                1. HEAP[TOP] = -HEAP[TOP]
        """
        file.write("UMEN")
        pass

    # Logical operations
    @staticmethod
    def _and(file: TextIOWrapper):
        """
            Write CONJ.
            Do:

                1. IF HEAP[TOP - 1] = 1 AND HEAP[TOP] = 1 THEN HEAP[TOP - 1] = 1; ELSE HEAP[TOP - 1] = 0 
                2. TOP = TOP - 1
        """
        file.write("CONJ")
        pass

    @staticmethod
    def _or(file: TextIOWrapper):
        """
            Write DISJ.
            Do:

                1. IF HEAP[TOP - 1] = 1 or HEAP[TOP] = 1 THEN HEAP[TOP - 1] = 1; ELSE HEAP[TOP - 1] = 0 
                2. TOP = TOP - 1
        """
        file.write("DISJ")
        pass

    @staticmethod
    def _not(file: TextIOWrapper):
        """
            Write NEGA.
            Do:

                1. IF HEAP[TOP] = HEAP[TOP] - 1
        """
        file.write("NEGA")
        pass
    
    # Comparisson operations
    @staticmethod
    def lt(file: TextIOWrapper):
        """
            Write CMME.
            Do:

                1. IF HEAP[TOP - 1] < HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        file.write("CMME")
        pass

    @staticmethod
    def gt(file: TextIOWrapper):
        """
            Write CMMA.
            Do:

                1. IF HEAP[TOP - 1] > HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        file.write("CMMA")
        pass

    @staticmethod
    def eq(file: TextIOWrapper):
        """
            Write CMIG.
            Do:

                1. IF HEAP[TOP - 1] = HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        file.write("CMIG")
        pass

    @staticmethod
    def neq(file: TextIOWrapper):
        """
            Write CMDG.
            Do:

                1. IF HEAP[TOP - 1] <> HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        file.write("CMDG")
        pass

    @staticmethod
    def leq(file: TextIOWrapper):
        """
            Write CMNI.
            Do:

                1. IF HEAP[TOP - 1] <= HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        file.write("CMNI")
        pass

    @staticmethod
    def gte(file: TextIOWrapper):
        """
            Write CMYI.
            Do:

                1. IF HEAP[TOP - 1] >= HEAP[TOP] THEN HEAP[TOP - 1] = 1 ELSE HEAP[TOP - 1] = 0
                2. TOP = TOP - 1
        """
        file.write("CMYI")
        pass

    # Jump instructions
    @staticmethod
    def jump(file: TextIOWrapper, label:str ):
        """
            Write DSVS label.
            Do:
                
                1. i = LABEL_HASHMAP[label]
        """
        file.write(f"APCT {label}")
        pass

    # Jump instructions
    @staticmethod
    def jmp(file: TextIOWrapper, label:str ):
        """
            Write DSVS label.
            Do:
                
                1. i = LABEL_HASHMAP[label]
        """
        file.write(f"DSVS {label}")
        pass
    
    @staticmethod
    def jz(file: TextIOWrapper, label:str ):
        """
            Write DSVF label.
            Do:
                
                1. IF HEAP[TOP] = 0 THEN i = LABEL_HASHMAP[label] ELSE i = i + 1
                2. TOP = TOP - 1
        """
        file.write(f"DSVF {label}")
        pass

    @staticmethod
    def nop(file: TextIOWrapper, label:str ):
        """
            Write label NADA.
            Do:
                1. LABEL_HASHMAP[label] = i - 1 
        """
        file.write(f"{label} NADA")
        pass
    
    # Read/write instruction
    @staticmethod
    def read(file: TextIOWrapper):
        """
            Write LEER.
            Do:
                1. TOP = TOP + 1
                2. HEAP[TOP] = input sent by stream
        """
        file.write(f"LEER")
        pass

    @staticmethod
    def write(file: TextIOWrapper):
        """
            Write IMPR
            Do:

                1. print HEAP[TOP]
                2. TOP = TOP - 1
        """
        file.write(f"IMPR")
        pass

    # Push instructions
    @staticmethod
    def push_c(file: TextIOWrapper, constant_value:str ):
        """
            Write APCT constant_value.
            Do:
        
                1. TOP = TOP + 1
                1. HEAP[TOP] = constant_value
        """
        file.write(f"APCT {constant_value}")
        pass
    
    @staticmethod
    def push_v(file: TextIOWrapper, scope_level: int ,variable_offset: int ):
        """
            Write APVL scope_level, variable_offset.
            Do:
                
                1. TOP = TOP + 1
                2. HEAP[TOP] = HEAP[DISPLAY[scope_level] + variable_offset ]
        """
        file.write(f"APVL {scope_level}, {variable_offset}")
        pass
    
    # Store
    @staticmethod
    def store(file: TextIOWrapper, scope_level: int ,variable_offset: int ):
        """
            Write ALVL scope_level, variable_offset.
            Do:
                
                1. HEAP[DISPLAY[scope_level] + variable_offset ] = HEAP[TOP]
                2. TOP = TOP - 1
        """
        file.write(f"ALVL {scope_level}, {variable_offset}")
        pass
    
    # Programs and procedures
    @staticmethod
    def init(file: TextIOWrapper):
        """
            Write INPP.
            Do:
                
                1. TOP = - 1
                2. DISPLAY[0] = 0
        """
        file.write("INPP")
        pass
    
    @staticmethod
    def enter(file: TextIOWrapper, procedure_level: int):
        """
            Write ENPR procedure_level.
            Do:
                
                1. TOP = TOP + 1
                2. HEAP[TOP] = DISPLAY[procedure_level]
                3. DISPLAY[procedure_level] = TOP + 1
        """
        file.write(f"ENPR {procedure_level}")
        pass
    
    @staticmethod
    def call(file: TextIOWrapper, procedure_label: int):
        """
            Write LLPR procedure_level.
            Do:
                
                1. TOP = TOP + 1
                2. HEAP[TOP] = i + 1
                3. i = LABEL_HASHMAP[procedure_label]
        """
        file.write(f"LLPR {procedure_label}")
        pass
    
    @staticmethod
    def memloc(file: TextIOWrapper, memory_to_alloc: int):
        """
            Write RMEM memory_to_alloc.
            Do:
                
                1. TOP = TOP + memory_to_alloc
                
        """
        file.write(f"RMEM {memory_to_alloc}")
        pass
    
    @staticmethod
    def free(file: TextIOWrapper, memory_to_free: int):
        """
            Write LMEM memory_to_free.
            Do:
                
                1. TOP = TOP - memory_to_free
        """
        file.write(f"LMEM {memory_to_free}")
        pass
    
    @staticmethod
    def _return(file: TextIOWrapper, procedure_level: int, memory_required_by_parameters: int):
        """
            Write RTPR procedure_level, memory_required_by_parameters.
            Do:
                
                1. DISPLAY[procedure_level] = HEAP[TOP]
                2. i = HEAP[TOP - 1]
                1. TOP = TOP - (memory_required_by_parameters + 2)
        """
        file.write(f"RTPR {procedure_level}, {memory_required_by_parameters}")
        pass
    
    @staticmethod
    def halt(file: TextIOWrapper):
        """
            Write PARA.
        """
        file.write("PARA")
        pass

    pass