"""
Othello game example.
Prints board state to stdout with random agents by default.
"""

import re
import sys
import colorama
import numpy as np

from fights.base import BaseAgent
from fights.envs import othello

from minimax_agent import MinimaxAgent

sys.path.append("../")


class RandomAgent(BaseAgent):
    """
    Just random agent
    """
    env_id = ("othello", 0)  # type: ignore

    def __init__(self, agent_id: int, seed: int = 0) -> None:
        self.agent_id = agent_id  # type: ignore
        self._rng = np.random.default_rng(seed)

    def _get_all_actions(self, state: othello.OthelloState):
        actions = []
        for cx in range(othello.OthelloEnv.board_size):
            for cy in range(othello.OthelloEnv.board_size):
                action = [cx, cy]
                if state.legal_actions[self.agent_id][cx][cy]:
                    actions.append(action)
        return actions

    def __call__(self, state: othello.OthelloState) -> othello.OthelloAction:
        actions = self._get_all_actions(state)
        return self._rng.choice(actions)


def fallback_to_ascii(s: str) -> str:
    """
    for the windows env
    """
    try:
        s.encode(sys.stdout.encoding)
    except UnicodeEncodeError:
        s = re.sub("[┌┬┐├┼┤└┴┘╋]", "+", re.sub("[─━]", "-", re.sub("[│┃]", "|", s)))
    return s


def run():
    """
    Just run the othello environment with two random agents.
    """
    assert othello.OthelloEnv.env_id == RandomAgent.env_id
    colorama.init()

    state = othello.OthelloEnv().initialize_state()
    agents = [RandomAgent(0), RandomAgent(1)]

    print("\x1b[2J")

    step_num = 0
    while not state.done:

        print("\x1b[1;1H")
        print(fallback_to_ascii(str(state)))

        for agent in agents:

            action = agent(state)
            state = othello.OthelloEnv().step(state, agent.agent_id, action)

            print("\x1b[1;1H")
            print(fallback_to_ascii(str(state)))

            pause = input()

            if state.done:
                print(f"agent {np.argmax(state.reward)} \
                    won in {step_num} iters")
                break

        step_num += 1


if __name__ == "__main__":
    run()
