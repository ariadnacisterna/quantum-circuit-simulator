from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, model_validator


class GateType(str, Enum):
    H = "H"
    X = "X"
    CNOT = "CNOT"


class QubitCount(int, Enum):
    TWO = 2
    THREE = 3
    FOUR = 4


class SingleGate(BaseModel):
    type: Literal[GateType.H, GateType.X]
    qubit: Annotated[int, Field(ge=0, le=3)]
    step: Annotated[int, Field(ge=0)]


class CnotGate(BaseModel):
    type: Literal[GateType.CNOT]
    control: Annotated[int, Field(ge=0, le=3)]
    target: Annotated[int, Field(ge=0, le=3)]
    step: Annotated[int, Field(ge=0)]

    @model_validator(mode="after")
    def control_and_target_differ(self) -> "CnotGate":
        if self.control == self.target:
            raise ValueError("control and target qubits must differ")
        return self


Gate = Annotated[Union[SingleGate, CnotGate], Field(discriminator="type")]


class SimulationRequest(BaseModel):
    qubit_count: QubitCount
    gates: Annotated[list[Gate], Field(min_length=1, max_length=64)]

    @model_validator(mode="after")
    def gates_within_qubit_range(self) -> "SimulationRequest":
        n = int(self.qubit_count)
        for gate in self.gates:
            if isinstance(gate, SingleGate) and gate.qubit >= n:
                raise ValueError(
                    f"gate targets qubit {gate.qubit} but circuit has only {n} qubits"
                )
            if isinstance(gate, CnotGate):
                if gate.control >= n or gate.target >= n:
                    raise ValueError(
                        f"CNOT references qubit index outside range [0, {n - 1}]"
                    )
        return self


class ProbabilityResult(BaseModel):
    state: str
    probability: float = Field(ge=0.0, le=1.0)


class SimulationResponse(BaseModel):
    results: list[ProbabilityResult]
    total_shots: int
    execution_time_ms: float