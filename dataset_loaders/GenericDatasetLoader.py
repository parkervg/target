from dataset_loaders.AbsTargetDatasetLoader import AbsTargetDatasetLoader
from pathlib import Path
from datasets import load_dataset, DatasetDict
class GenericDatasetLoader(AbsTargetDatasetLoader):
    def __init__(self,
                 dataset_name: str,
                 dataset_path: str,
                 datafile_ext: str = None,
                 table_col_name: str = "table",
                 table_id_col_name: str = "table_id",
                 splits: str | list[str] = "test",
                 data_directory: str = None,
                 query_type: str = "",
                 ):
        '''
        Constructor for a generic dataset loader that loads from a local directory

        Parameters:
            dataset_path (str): the path to the directory where the dataset files reside. an example dataset files orgnanization for target:
                dataset_path/
                ├── corpus/
                │   ├── train.csv
                │   └── test.csv
                └── queries/
                    ├── train.csv
                    └── test.csv
            Dataset file formats supported: csv, json, parquet, etc
        '''
        super().__init__(
            dataset_name=dataset_name, 
            table_col_name=table_col_name,
            table_id_col_name=table_id_col_name,
            splits=splits,
            data_directory=data_directory,
            query_type=query_type
        )
        self.dataset_path = Path(dataset_path)
        self.corpus_path = self.dataset_path / "corpus"
        self.queries_path = self.dataset_path / "queries"
        self.datafile_ext = datafile_ext

    def load(self, splits: str | list[str] = None) -> None:
        '''
        Load specific splits of a dataset, such as 'train', 'test', or 'validation'. It can accept either a single split as a string or a list of splits.

        Parameters:
            split(str | list[str], optional): The dataset split or splits to load. Defaults to None, which will load test split or the split specified when constructing this Generic Dataset Loader object
        '''
        if splits:
            if isinstance(splits, str):
                splits = [splits]
            for split in splits: 
                if split not in self.splits:
                    self.splits.append(split)
        self._load_corpus()
        self._load_queries()
        

    def _load_corpus(self) -> None:
        if not self.corpus:
            self.corpus = DatasetDict()
        for split in self.splits:
            if split not in self.corpus:
                self.corpus[split] = load_dataset(path=str(self.corpus_path), split=split)

    def _load_queries(self) -> None:
        if not self.queries:
            self.queries = DatasetDict()
        for split in self.splits:
            if split not in self.queries:
                self.queries[split] = load_dataset(path=str(self.queries_path), split=split)
