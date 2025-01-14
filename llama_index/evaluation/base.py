"""Evaluator."""
from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence

from llama_index.bridge.pydantic import BaseModel, Field
from llama_index.response.schema import Response


class EvaluationResult(BaseModel):
    """Evaluation result.

    Output of an BaseEvaluator.
    """

    query: Optional[str] = Field(None, description="Query string")
    contexts: Optional[Sequence[str]] = Field(None, description="Context strings")
    response: Optional[str] = Field(None, description="Response string")
    passing: Optional[bool] = Field(
        None, description="Binary evaluation result (passing or not)"
    )
    feedback: Optional[str] = Field(
        None, description="Feedback or reasoning for the response"
    )
    score: Optional[float] = Field(None, description="Score for the response")


class BaseEvaluator(ABC):
    """Base Evaluator class."""

    @abstractmethod
    def evaluate(
        self,
        query: Optional[str] = None,
        response: Optional[str] = None,
        contexts: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        """Run evaluation with query string, retrieved contexts,
        and generated response string.

        Subclasses can override this method to provide custom evaluation logic and
        take in additional arguments.
        """
        raise NotImplementedError

    def evaluate_response(
        self,
        query: Optional[str] = None,
        response: Optional[Response] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        """Run evaluation with query string and generated Response object.

        Subclasses can override this method to provide custom evaluation logic and
        take in additional arguments.
        """
        response_str: Optional[str] = None
        contexts: Optional[Sequence[str]] = None
        if response is not None:
            response_str = response.response
            contexts = [node.get_content() for node in response.source_nodes]

        return self.evaluate(
            query=query, response=response_str, contexts=contexts, **kwargs
        )


# legacy: backward compatibility
Evaluation = EvaluationResult
