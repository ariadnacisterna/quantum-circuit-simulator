export type GateType = "H" | "X" | "CNOT";

export type QubitCount = 2 | 3 | 4;

export interface SingleGate {
  type: Extract<GateType, "H" | "X">;
  qubit: number;
  step: number;
}

export interface CnotGate {
  type: Extract<GateType, "CNOT">;
  control: number;
  target: number;
  step: number;
}

export type Gate = SingleGate | CnotGate;

export interface CircuitCell {
  qubit: number;
  step: number;
  gate: GateType | null;
  isControl?: boolean;
  isTarget?: boolean;
}

export interface CircuitState {
  qubitCount: QubitCount;
  stepCount: number;
  gates: Gate[];
}

export interface SimulationRequest {
  qubit_count: QubitCount;
  gates: Gate[];
}

export interface ProbabilityResult {
  state: string;
  probability: number;
}

export interface SimulationResponse {
  results: ProbabilityResult[];
  total_shots: number;
  execution_time_ms: number;
}

export type SimulationStatus = "idle" | "loading" | "success" | "error";

export interface SimulationState {
  status: SimulationStatus;
  response: SimulationResponse | null;
  error: string | null;
}

export interface GatePaletteItem {
  type: GateType;
  label: string;
  description: string;
  color: string;
}