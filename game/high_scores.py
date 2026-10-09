import json
from pathlib import Path

class HighScores:
    def __init__(self,path=None):
        self.path=Path(path) if path is not None else Path(__file__).resolve().parents[1]/"high_scores.json"
        self.error=None
        try:
            data=json.loads(self.path.read_text())
            self.scores=sorted([n for n in data if type(n) is int and n>=0],reverse=True)[:5] if isinstance(data,list) else []
        except (OSError,ValueError):
            self.scores=[]

    def add(self,score):
        self.scores=sorted(self.scores+[score],reverse=True)[:5]
        try:
            temp=self.path.with_suffix('.tmp')
            temp.write_text(json.dumps(self.scores,indent=2))
            temp.replace(self.path)
            self.error=None
        except OSError:
            self.error="Scores could not be saved"
