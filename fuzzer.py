from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import PGGCFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer
import grammar
import random 

class MyFuzzer(PGGCFuzzer):
    def choose_node_expansion(self, node, children_alternatives):
        return random.randrange(0, len(children_alternatives))
        
class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
    
    def setup_fuzzer(self):
        # This function may be changed.
        self.fuzzer = MyFuzzer(self.grammar)

    def fuzz_one_input(self) -> str:
        # This function should be implemented, but the signature may not change.
        fuzz_input = self.fuzzer.fuzz()
        return fuzz_input