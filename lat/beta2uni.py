#!/usr/bin/env python

import re

def betadict(char):
    return {
        'a' : 'α',
        'b' : 'β',
        'g' : 'γ',
        'd' : 'δ',
        'e' : 'ε',
        'v' : 'ϝ',
        'z' : 'ζ',
        'h' : 'η',
        'q' : 'θ',
        'i' : 'ι',
        'k' : 'κ',
        'l' : 'λ',
        'm' : 'μ',
        'n' : 'ν',
        'c' : 'ξ',
        'o' : 'ο',
        'p' : 'π',
        'r' : 'ρ',
        's' : 'σ',
        't' : 'τ',
        'u' : 'υ',
        'f' : 'φ',
        'x' : 'χ',
        'y' : 'ψ',
        'w' : 'ω',
        '(' : "\u0314",
        ')' : "\u0313",
        '/' : "\u0341",
        '=' : "\u0342",
        "\\": "\u0340",
        '+' : "\u0308",
        '|' : "\u0345",
        '&' : "\u0304",
        "'" : "\u0306"
    }.get(char, char)

def beta_to_uni(betastring):
    newstring = re.sub(r"(^|\s)([()=\\/]*)(\*)*([()=\\/]*)(\w)", r"\1\3\5\2\4", betastring)
    sigmastring = re.sub(r"s\b", r"ς", newstring)
    answer_arr = []
    capitalize = False
    for i in sigmastring:
        if i == "*":
            capitalize = True
        elif capitalize and i.isalpha:
            answer_arr.append(betadict(i).capitalize())
            capitalize = False
        else:
            answer_arr.append(betadict(i))
    return ''.join(answer_arr)