class NonDeterministicFiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = dict()
        self.initial_state = None
        self.final_states = set()

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

            print("\n========================================")
            print(file_path + " carregado!")
            print("========================================")

            self.initial_state = lines[0].strip()

            alphabet_symbols = lines[1].strip().split(' ')
            self.alphabet = set(alphabet_symbols)

            all_states = lines[2].strip().split(' ')
            self.states = set(all_states)

            final_state_symbols = lines[3].strip().split(' ')
            self.final_states = set(final_state_symbols)

            for line in lines[4:]:
                from_state, to_states, symbol = line.strip().split(' ')
                transition_key = (from_state, symbol)
                to_state_array = to_states.split(',')
                self.transitions[transition_key] = to_state_array

            print("Transições =>\n\n", self.transitions)
            print("\n========================================")

    def run(self, input_word):
        current_states = {self.initial_state}

        for symbol in input_word:
            new_states = set()

            for state in current_states:
                transition_key = (state,symbol)

                if transition_key in self.transitions:
                    transition_states = self.transitions[transition_key]
                    new_states.update(transition_states)

                epsilon_transition_key = (state,'&')
                if epsilon_transition_key in self.transitions:
                    epsilon_transition_states = self.transitions[epsilon_transition_key]
                    new_states.update(epsilon_transition_states)

            current_states = new_states

        for state in current_states:
            if state in self.final_states:
                print("Estado Final =>", state)
                return 'Aceita'
        
        print("Estado Final =>", state)
        return 'Rejeitada'

def main():
    automaton = NonDeterministicFiniteAutomaton()
    file_path = 'automatoAFN.txt'

    automaton.load_from_file(file_path)

    input_word = input('Digite uma palavra: ')
    result = automaton.run(input_word)
    print(result)

if __name__ == "__main__":
    main()