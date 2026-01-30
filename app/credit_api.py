"""
Credit score provider interface.

Currently uses manual entry (user provides their own score).
This module defines the interface for future integration with
credit bureau APIs (Experian, Equifax, TransUnion).
"""

from abc import ABC, abstractmethod


class CreditProvider(ABC):
    """Abstract interface for credit score providers."""

    @abstractmethod
    def get_score(self, user_identifier: str) -> dict:
        """
        Retrieve a credit score.

        Args:
            user_identifier: Provider-specific identifier (e.g. SSN, account ID)

        Returns:
            dict with keys: score (int), source (str)
        """
        pass


class ManualEntryProvider(CreditProvider):
    """User provides their own credit score (PoC)."""

    def get_score(self, user_identifier: str) -> dict:
        raise NotImplementedError(
            "ManualEntryProvider does not fetch scores. "
            "Score should be provided directly by the user."
        )


class MockAPIProvider(CreditProvider):
    """Simulated credit bureau API for testing."""

    def __init__(self, default_score: int = 720):
        self.default_score = default_score

    def get_score(self, user_identifier: str) -> dict:
        return {
            "score": self.default_score,
            "source": "mock_api",
        }


# Placeholder for real API integrations:
#
# class ExperianProvider(CreditProvider):
#     def __init__(self, api_key: str, api_url: str):
#         self.api_key = api_key
#         self.api_url = api_url
#
#     def get_score(self, user_identifier: str) -> dict:
#         # Call Experian API
#         pass
#
# class EquifaxProvider(CreditProvider): ...
# class TransUnionProvider(CreditProvider): ...
