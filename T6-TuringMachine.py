class TuringMachine:
    def __init__(self, states, alphabet, tape_alphabet, initial_state, accept_state, reject_state, transitions):
        self.states = states
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.initial_state = initial_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.transitions = transitions
        self.head_position = 0
        self.tape = ['&']

    def run(self, input_string):
        current_state = self.initial_state
        self.tape = list(input_string)

        while current_state != self.accept_state and current_state != self.reject_state:
            current_symbol = self.tape[self.head_position]

            if (current_state, current_symbol) not in self.transitions:
                break

            next_state, write_symbol, move_direction = self.transitions[(current_state, current_symbol)]

            self.tape[self.head_position] = write_symbol
            if move_direction == 'R':
                self.head_position += 1
                if self.head_position == len(self.tape):
                    self.tape.append('&')
            elif move_direction == 'L':
                self.head_position = max(0, self.head_position - 1)

            current_state = next_state

        return current_state == self.accept_state

def main():
    states = {'q0', 'q1', 'q2', 'qaccept', 'qreject'}
    alphabet = {'0', '1'}
    tape_alphabet = {'0', '1', '&'}
    initial_state = 'q0'
    accept_state = 'qaccept'
    reject_state = 'qreject'

    transitions = {
        ('q0', '0'): ('q0', '0', 'R'),
        ('q0', '1'): ('q1', '1', 'R'),
        ('q1', '0'): ('q1', '0', 'R'),
        ('q1', '1'): ('q2', '1', 'R'),
        ('q2', '1'): ('q2', '1', 'R'),
        ('q2', '&'): ('qaccept', '&', 'L')
    }

    tm = TuringMachine(states, alphabet, tape_alphabet, initial_state, accept_state, reject_state, transitions)

    input_string = '000111'
    result = tm.run(input_string)

    if result:
        print(f'A entrada "{input_string}" foi aceita.')
    else:
        print(f'A entrada "{input_string}" foi rejeitada.')
    
if __name__ == "__main__":
    main()