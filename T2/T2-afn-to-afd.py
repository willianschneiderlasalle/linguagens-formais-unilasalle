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

        dfa = NonDeterministicFiniteAutomaton()
        dfa.initial_state = self.initial_state
        dfa.states.add(dfa.initial_state)

        helper : bool = True
        previous_visited = []

        while helper:
            temp_states = set()
            temp_visited = []
            
            for a in dfa.states:
                temp_visited.append(a)
                temp_states.add(a)
                temp_states.add(self.get_states(a))

            if previous_visited == temp_visited:
                helper = False
            else:
                previous_visited = temp_visited
                
            dfa.states = temp_states

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            current_state = stack.pop()
            epsilon_transitions = set(self.transitions.get((current_state, '&'), set()))
            
            new_states = epsilon_transitions - closure
            closure.update(new_states)
            stack.extend(new_states)

        return frozenset(closure)

    def convert_to_afd(self):
        afn_states = self.states
        afn_alphabet = self.alphabet
        afn_transitions = self.transitions
        afn_initial_state = self.initial_state
        afn_final_states = self.final_states

        afd = NonDeterministicFiniteAutomaton()
        afd.initial_state = self.epsilon_closure({afn_initial_state})

        unprocessed_states = [afd.initial_state]
        processed_states = set()

        while unprocessed_states:
            current_afd_state = unprocessed_states.pop()
            
            if current_afd_state:
                processed_states.add(current_afd_state)

                for symbol in afn_alphabet:
                    next_afn_states = set()

                    for state in current_afd_state:
                        next_afn_states.update(afn_transitions.get((state, symbol), set()))

                    next_afd_state = frozenset(next_afn_states)

                    if next_afd_state not in processed_states:
                        unprocessed_states.append(next_afd_state)

                    afd.transitions.setdefault(current_afd_state, dict())[symbol] = next_afd_state

                if any(state in afn_final_states for state in current_afd_state):
                    afd.final_states.add(current_afd_state)

                afd.states.add(current_afd_state)

        return {
            'states': afd.states,
            'alphabet': afn_alphabet,
            'transitions': afd.transitions,
            'initial_state': afd.initial_state,
            'final_states': afd.final_states
        }

def print_afd(afd):
    print("Estados do AFD:", [list(state) for state in afd['states']])
    print("Alfabeto do AFD:", afd['alphabet'])
    print("Transições do AFD:", {tuple(list(k)): {tuple(list(k2)): v2 for k2, v2 in v.items()} for k, v in afd['transitions'].items()})
    print("Estado Inicial do AFD:", list(afd['initial_state']))
    print("Estados Finais do AFD:", [list(state) for state in afd['final_states']])

def main():
    afn = NonDeterministicFiniteAutomaton()
    file_path = 'automatoAFN.txt'

    afn.load_from_file(file_path)

    while True:
        print("\nEscolha uma opção:")
        print("1. Testar palavra no AFN")
        print("2. Converter AFN para AFD")
        print("3. Sair")

        option = input("Opção: ")

        if option == '1':
            input_word = input('Digite uma palavra: ')
            result = afn.run(input_word)
            print(result)
        elif option == '2':
            afd_resultante = afn.convert_to_afd()
            print_afd(afd_resultante)
        elif option == '3':
            break

if __name__ == "__main__":
    main()