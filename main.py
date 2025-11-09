from dataclasses import dataclass
import os
import pandas as pd

try:
    import caas_jupyter_tools as cj
except Exception:
    class _FallbackCJ:
        @staticmethod
        def display_dataframe_to_user(title, df):
            safe_title = title.replace(' ', '_').replace("'", "")
            # Save CSV into the workspace-local ./output folder and print a short preview
            output_dir = os.path.join(os.path.dirname(__file__), "output")
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception:
                pass
            path = os.path.join(output_dir, f"{safe_title}.csv")
            try:
                df.to_csv(path, index=False)
                print(f"[Fallback] Saved dataframe '{title}' to: {path}")
            except Exception as e:
                print(f"[Fallback] Could not save CSV: {e}")
            # Print a small preview to console
            try:
                print('\n' + title)
                print(df.head(10).to_string(index=False))
            except Exception as e:
                print(f"[Fallback] Could not print dataframe preview: {e}")

    cj = _FallbackCJ()

BLANK = "⊔"  # Unicode blank symbol

@dataclass
class Transition:
    write: str
    move: str   # 'L', 'R', or 'S'
    next_state: str

class TuringMachine:
    def __init__(self, transitions, start_state="q0", halt_states=("HALT",)):
        self.transitions = transitions          # dict[(state, read)] -> Transition
        self.state = start_state
        self.halt_states = set(halt_states)
        self.tape = {}                           # sparse tape: index -> symbol
        self.head = 0                            # head starts at position 0
        self.min_index = 0
        self.max_index = 0

    def read(self):
        return self.tape.get(self.head, BLANK)

    def write(self, symbol):
        self.tape[self.head] = symbol
        self.min_index = min(self.min_index, self.head)
        self.max_index = max(self.max_index, self.head)

    def run(self, max_steps=1000):
        log = []
        step_count = 0
        while step_count < max_steps and self.state not in self.halt_states:
            cur_state = self.state
            cur_head = self.head
            cur_read = self.read()
            key = (cur_state, cur_read)
            if key not in self.transitions:
                # No rule -> halt
                log.append({
                    "step": step_count,
                    "state": cur_state,
                    "head": cur_head,
                    "read": cur_read,
                    "write": None,
                    "move": None,
                    "next_state": "HALT",
                    "tape": self.snapshot()
                })
                self.state = "HALT"
                break

            tr = self.transitions[key]
            # Apply transition
            self.write(tr.write)
            # Move
            if tr.move == "L":
                self.head -= 1
            elif tr.move == "R":
                self.head += 1
            elif tr.move == "S":
                pass
            else:
                raise ValueError(f"Invalid move: {tr.move}")

            # Update state
            self.state = tr.next_state
            step_count += 1

            log.append({
                "step": step_count,
                "state": self.state,
                "head": self.head,
                "read": cur_read,
                "write": tr.write,
                "move": tr.move,
                "next_state": self.state,
                "tape": self.snapshot()
            })
        return pd.DataFrame(log)

    def snapshot(self, padding=2):
        left = self.min_index - padding
        right = self.max_index + padding
        cells = []
        for i in range(left, right + 1):
            sym = self.tape.get(i, BLANK)
            if i == self.head:
                cells.append(f"[{sym}]")
            else:
                cells.append(f" {sym} ")
        return "".join(cells)


# Program that writes "MATEO" on a blank tape:
letters = ["M", "A", "T", "E", "O"]
transitions = {}

for idx, letter in enumerate(letters):
    state = f"q{idx}"
    next_state = f"q{idx+1}"
    # On blank, write the letter, move Right, go to next state
    transitions[(state, BLANK)] = Transition(write=letter, move="R", next_state=next_state)
    # If we re-encounter the same letter (e.g., lingering), keep moving right until blank
    transitions[(state, letter)] = Transition(write=letter, move="R", next_state=state)

# Final state q5 -> HALT on blank (stay)
transitions[("q5", BLANK)] = Transition(write=BLANK, move="S", next_state="HALT")


tm = TuringMachine(transitions, start_state="q0", halt_states=("HALT",))
df_log = tm.run(max_steps=50)

# Save log to CSV and display using caas_jupyter_tools or fallback
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "tm_write_MATEO_log.csv")
df_log.to_csv(csv_path, index=False)
cj.display_dataframe_to_user("TM log - writes 'MATEO'", df_log)

# Print final tape and contiguous result
final_tape_snapshot = tm.snapshot(padding=0)
final_text = "".join(tm.tape.get(i, BLANK) for i in range(tm.min_index, tm.max_index + 1))
print("Final de la Cinta:")
print(final_tape_snapshot)
print("\nFinal sin Espacios:")
print(final_text)

print("\nCSV guardado en:", csv_path)
