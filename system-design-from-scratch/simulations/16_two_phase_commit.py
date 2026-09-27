from typing import List, Any

class TwoPhaseCommitCoordinator:
    def __init__(self, participants: List[Any]):
        self.participants = participants

    def execute_transaction(self) -> bool:
        # Phase 1: Prepare
        votes = [p.prepare() for p in self.participants]
        if all(votes):
            # Phase 2: Commit
            for p in self.participants:
                p.commit()
            return True
        else:
            # Phase 2: Abort
            for p in self.participants:
                p.abort()
            return False
