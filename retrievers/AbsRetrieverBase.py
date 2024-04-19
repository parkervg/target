from abc import ABC, abstractmethod
from retrievers.RetrieversDataModels import RetrievalResultDataModel


class AbsRetrieverBase(ABC):
    """
    A base class for all Target Retrievers. Serves as a organization class, no function signatures are defined here, delegated to `AbsTargetRetrieverFree` and `AbsTargetRetrieverCon
    """

    @abstractmethod
    def retrieve(self, *args, **kwargs) -> list[str]:
        """
        The essential function for any Target Retriever. User have to implement this for the retriever class to work with evaluation pipeline.
        Returns:
            a dictionary mapping the query IDs to the list of possible tables retrieved.
        """
        pass

    @abstractmethod
    def retrieve_batch(self, *args, **kwargs) -> list[RetrievalResultDataModel]:
        pass