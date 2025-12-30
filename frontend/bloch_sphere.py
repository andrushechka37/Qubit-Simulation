from backend.session_state import get_circuit_instance

qc = get_circuit_instance()
qc.draw_bloch_sphere()
