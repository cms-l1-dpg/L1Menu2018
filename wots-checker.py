#!/usr/bin/env python2
#
# Wrath-of-the-samurai (WotS) checker
#
# Checks XML menus for condition expression hash collisions.
#

import tmEventSetup
import tmGrammar

import argparse
import sys, os

def parse(expression):
    """Split algorithm expression into tokens,
    as done in esTriggerMenuHandle::parse().
    """
    tmGrammar.Algorithm_Logic.clear()
    if not tmGrammar.Algorithm_parser(expression):
        raise RuntimeError(expression)
    return tmGrammar.Algorithm_Logic.getTokens()

def analyze(filename):
    """Test an XML menu for condition expression hash collisions."""
    eventsetup = tmEventSetup.getTriggerMenu(filename)

    algorithms = eventsetup.getAlgorithmMapPtr()

    conditions = {}

    for name, algorithm in algorithms.items():
        tokens = parse(algorithm.getExpression())
        for token in tokens:
            hashulong = tmEventSetup.getHashUlong(token)
            if not hashulong in conditions.keys():
                conditions[hashulong] = set()
            conditions[hashulong].add(token)

    errors = []

    for hashulong, tokens in conditions.items():
        if len(tokens) > 1:
            errors.append((hashulong, tokens))

    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()

    fails = 0

    for filename in args.filenames:
        print ">>> checking", filename
        errors = analyze(filename)
        if errors:
	    for error in errors:
            # Add some color...
	        if sys.stdout.isatty():
	            sys.stdout.write("\033[31m")
	        print "ERROR>>", error[0], error[1]
	        if sys.stdout.isatty():
	            sys.stdout.write("\033[0m")
	            sys.stdout.flush()
            fails += 1
	    print len(errors), "errors." if len(errors) > 1 else "error."

    if fails:
        print fails, "checks failed."
    else:
        print "ALL OK."
