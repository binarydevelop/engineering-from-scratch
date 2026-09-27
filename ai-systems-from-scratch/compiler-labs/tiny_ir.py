"""
Tiny IR and SSA Representation (Phases 18-22).
Implements a textual Intermediate Representation (IR), Static Single Assignment (SSA) values,
canonicalization, and pattern rewriting rules.
"""

from typing import List, Dict, Tuple, Optional

class SSAValue:
    def __init__(self, id_num: int, dtype: str = "f32", shape: Tuple[int, ...] = ()):
        self.name = f"%{id_num}"
        self.dtype = dtype
        self.shape = shape

    def __repr__(self):
        return f"{self.name}: {self.dtype}{list(self.shape)}"

class Instruction:
    def __init__(self, result: SSAValue, op: str, operands: List[SSAValue], attributes: Optional[Dict] = None):
        self.result = result
        self.op = op
        self.operands = operands
        self.attributes = attributes or {}

    def __repr__(self):
        ops_str = ", ".join(op.name for op in self.operands)
        attr_str = f" {self.attributes}" if self.attributes else ""
        return f"{self.result.name} = {self.op}({ops_str}){attr_str}"

class TinyIRModule:
    def __init__(self):
        self.val_counter = 0
        self.instructions: List[Instruction] = []

    def new_val(self, dtype: str = "f32", shape: Tuple[int, ...] = ()) -> SSAValue:
        v = SSAValue(self.val_counter, dtype, shape)
        self.val_counter += 1
        return v

    def emit(self, op: str, operands: List[SSAValue], dtype: str = "f32", shape: Tuple[int, ...] = (), attributes: Optional[Dict] = None) -> SSAValue:
        res = self.new_val(dtype, shape)
        inst = Instruction(res, op, operands, attributes)
        self.instructions.append(inst)
        return res

    def to_string(self) -> str:
        lines = ["module {", "  func @forward() {"]
        for inst in self.instructions:
            lines.append(f"    {inst}")
        lines.append("  }")
        lines.append("}")
        return "\n".join(lines)

    def canonicalize(self) -> int:
        """
        Compiler pass: Canonicalizes commutative operations into a deterministic order.
        For commutative ops like 'add' and 'mul', sort operands by SSA ID string.
        """
        changes = 0
        for inst in self.instructions:
            if inst.op in ("add", "mul") and len(inst.operands) == 2:
                if inst.operands[0].name > inst.operands[1].name:
                    inst.operands = [inst.operands[1], inst.operands[0]]
                    changes += 1
        return changes

    def pattern_rewrite(self) -> int:
        """
        Compiler pass: Replaces algebraic identities:
        - mul(%x, %one) -> %x
        - add(%x, %zero) -> %x
        """
        changes = 0
        replacement: Dict[str, SSAValue] = {}
        new_instructions: List[Instruction] = []

        for inst in self.instructions:
            # Update operands
            inst.operands = [replacement.get(op.name, op) for op in inst.operands]

            # Identity rules:
            if inst.op == "mul" and "constant_val" in inst.attributes and inst.attributes["constant_val"] == 1.0:
                # Identity multiplication
                replacement[inst.result.name] = inst.operands[0]
                changes += 1
                continue
            elif inst.op == "add" and "constant_val" in inst.attributes and inst.attributes["constant_val"] == 0.0:
                replacement[inst.result.name] = inst.operands[0]
                changes += 1
                continue

            new_instructions.append(inst)

        self.instructions = new_instructions
        return changes
