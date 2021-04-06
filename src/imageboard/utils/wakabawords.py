import re
import random


grammar = {
    'W': ['%C%%T%', '%C%%T%', '%C%%X%', '%C%%D%%F%', '%C%%V%%F%%T%', '%C%%D%%F%%U%', '%C%%T%%U%', '%I%%T%', '%I%%C%%T%', '%A%'],
    'A': ['%K%%V%%K%%V%tion'],
    'K': ['b', 'c', 'd', 'f', 'g', 'j', 'l', 'm', 'n', 'p', 'qu', 'r', 's', 't', 'v', 's%P%'],
    'I': ['ex', 'in', 'un', 're', 'de'],
    'T': ['%V%%F%', '%V%%E%e'],
    'U': ['er', 'ish', 'ly', 'en', 'ing', 'ness', 'ment', 'able', 'ive'],
    'C': ['b', 'c', 'ch', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'qu', 'r', 's', 'sh', 't', 'th', 'v', 'w', 'y', 's%P%', '%R%r', '%L%l'],
    'E': ['b', 'c', 'ch', 'd', 'f', 'g', 'dg', 'l', 'm', 'n', 'p', 'r', 's', 't', 'th', 'v', 'z'],
    'F': ['b', 'tch', 'd', 'ff', 'g', 'gh', 'ck', 'll', 'm', 'n', 'n', 'ng', 'p', 'r', 'ss', 'sh', 't', 'tt', 'th', 'x', 'y', 'zz', 'r%R%', 's%P%', 'l%L%'],
    'P': ['p', 't', 'k', 'c'],
    'Q': ['b', 'd', 'g'],
    'L': ['b', 'f', 'k', 'p', 's'],
    'R': ['%P%', '%Q%', 'f', 'th', 'sh'],
    'V': ['a', 'e', 'i', 'o', 'u'],
    'D': ['aw', 'ei', 'ow', 'ou', 'ie', 'ea', 'ai', 'oy'],
    'X': ['e', 'i', 'o', 'aw', 'ow', 'oy'],
}


def make_word(cur='%W%', level=0, debug=False):
    def replacer(matchobj):
        grammar_key = matchobj.group(1)
        expansions = grammar[grammar_key]
        grammar_part = random.choice(expansions)

        if debug:
            print('{}{}: {}'.format(' ' * 4 * level, grammar_key, grammar_part))

        return make_word(grammar_part, level + 1, debug)

    return re.sub(r'%(\w+)%', replacer, cur)


if __name__ == '__main__':
    for _ in range(0, 50):
        print(make_word(debug=True))
