import asyncio

from ai.agents.analysis import AnalysisAgent


def test_analysis_agent_defaults():
    agent = AnalysisAgent()
    result = asyncio.run(agent.analyze([]))
    assert "budget" in result
