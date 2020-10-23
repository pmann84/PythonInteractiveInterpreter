#!/usr/bin/env python

import os
import sys
import unittest

# Add the pii module to the path
sys.path.insert(0, os.path.abspath(".."))

# Import the pii module
from pii import piilib


# Setup class for history tests
class PiiCommandHistoryTestSetup(unittest.TestCase):

    CMDS = ["foo", "blah", "test", "hello", "yes"]

    def setUp(self):
        # Instantiate a PiiCommandHistory object
        self.history = piilib.history.PiiCommandHistory()
        # Add 3 commands to history
        for cmd in self.CMDS:
            self.history.add_to_history(cmd)


class PiiCommandHistoryTests(PiiCommandHistoryTestSetup):

    def test_add_command_to_history(self):
        # Check that the history is length 3 and equal to the cmds list
        self.assertEqual(len(self.history.command_list), len(self.CMDS))
        self.assertEqual(self.history.command_list, self.CMDS)

    def test_get_previous_command(self):
        # run the prev command 3 times to get the commands
        for i in range(1, len(self.CMDS)):
            self.assertEqual(self.history.get_prev_command(), self.CMDS[-i])

    def test_get_previous_command_clamp(self):
        # run the prev command 2*(3+1) times to get the commands
        for i in range(2*len(self.CMDS)):
            returned_cmd = self.history.get_prev_command()
            curr_pos = self.history.history_pos
            if i < len(self.CMDS):
                self.assertEqual(returned_cmd, self.CMDS[curr_pos])
                self.assertEqual(curr_pos, len(self.CMDS)-i-1)
            else:
                self.assertEqual(returned_cmd, self.CMDS[0])
                self.assertEqual(curr_pos, 0)

    def test_get_next_command_from_start(self):
        # run the next command 3 times from the start to get empty always
        for i in range(1, len(self.CMDS)):
            self.assertEqual(self.history.get_next_command(), "")

    def test_get_next_command_from_previous_position(self):
        offset = 2
        num_left = len(self.CMDS)-offset
        # Go back a few commands
        for i in range(num_left):
            self.history.get_prev_command()

        # Now go forwards by the same amount
        for i in range(0, num_left):
            returned_cmd = self.history.get_next_command()
            if self.history.history_pos == len(self.CMDS)-1 and returned_cmd == "":
                self.assertEqual(returned_cmd, "")
            else:
                self.assertEqual(returned_cmd, self.CMDS[offset+i+1])

    def test_get_next_command_from_previous_position_clamped(self):
        offset = 2
        num_left = len(self.CMDS)-offset
        # Go back a few commands
        for i in range(num_left):
            self.history.get_prev_command()

        # Now go forwards by the same amount
        for i in range(0, num_left*4):
            returned_cmd = self.history.get_next_command()
            if self.history.history_pos >= len(self.CMDS)-1 and returned_cmd == "":
                self.assertEqual(returned_cmd, "")
            else:
                self.assertEqual(returned_cmd, self.CMDS[offset+i+1])

    def test_clear_history(self):
        self.history.clear_history()
        self.assertEqual(self.history.command_list, [])
        self.assertEqual(self.history.history_pos, -1)

# Run the tests with higher than default verbosity
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PiiCommandHistoryTests)
    unittest.TextTestRunner(verbosity=10).run(suite)
