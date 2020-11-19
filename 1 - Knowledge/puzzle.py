from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A must be a Knave or a Knight...
    Or(AKnave, AKnight),

    # ...but not both
    Not(And(AKnave, AKnight)),

    # If he is a Knight, he is telling the true,
    # so he must be both a Knight and a Knave
    Implication(AKnight, And(AKnight, AKnave)),

    # If he is a Knave, he is lying,
    # so he can't be both a Knight and a Knave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A must be a Knight or a Knave, so do B...
    And(Or(AKnave, AKnight), Or(BKnave, BKnight)),

    # ...but they can't be both
    And(Not(And(AKnave, AKnight)), Not(And(BKnave, BKnight))),

    # If A is a Knight, he is telling the true,
    # so A and B are Knaves
    Implication(AKnight, And(AKnave, BKnave)),

    # If A is a Knave, he is lying,
    # so they both can't be Knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A must be a Knight or a Knave, so do B...
    And(Or(AKnave, AKnight), Or(BKnave, BKnight)),

    # ...but they can't be both
    And(Not(And(AKnave, AKnight)), Not(And(BKnave, BKnight))),

    # If A is a Knight, he is telling the true,
    # so A and B are both Knights or Knaves
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # If A is a Knave, he is lying,
    # so they both can't be Knights or Knaves
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # If B is a Knight, he is telling the true,
    # so A and B are not the same
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    # If B is a Knave, he is lying,
    # so A and B are both Knights or Knaves
    Implication(BKnave,  Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A must be a Knight or a Knave, so do B an C...
    And(Or(AKnave, AKnight), Or(BKnave, BKnight), Or(CKnave, CKnight)),

    # ...but they can't be both
    And(Not(And(AKnave, AKnight)), Not(And(BKnave, BKnight)), Not(And(CKnave, CKnight))),

    # If A is a Knight, C is telling the true,
    # so A and C are Knights
    # B is lying about C, so he is a Knave
    Implication(AKnight, And(AKnight, BKnave, CKnight)),

    # If A is a Knave, C is lying,
    # so A and C are Knaves
    # B told the true about C, but lied about A,
    # because a Knave would not say he is a Knave,
    # so he is both a Knight and a Knave
    Implication(AKnave, And(AKnave, BKnight, BKnave, CKnave)),

    # If B is a Knight, he is telling the true,
    # so B is a Knight, A and C are Knaves
    Implication(BKnight, And(AKnave, BKnight, CKnave)),

    # If B are a Knave, he is lying,
    # so B is a Knave, A and C are not Knaves
    Implication(BKnave, And(Not(AKnave), BKnave, Not(CKnave))),

    # If C is a Knight, he is telling the true,
    # so C and A are Knights
    Implication(CKnight, And(AKnight, CKnight)),

    # If C is a Knave, he is lying,
    # so C and A are not Knights
    Implication(CKnave, And(Not(AKnight), Not(CKnight)))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
