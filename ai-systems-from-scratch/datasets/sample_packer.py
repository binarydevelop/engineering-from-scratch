"""
Sample Packing Simulator (Phase 88).
Concatenates multiple short token sequences into a single fixed-length
context window, generating sample-boundary position IDs and 2D block-diagonal
attention masks to prevent attention leakage across unrelated examples.
"""

from typing import List, Dict, Tuple
import torch

class SamplePacker:
    def __init__(self, max_seq_len: int = 128, pad_token_id: int = 0):
        self.max_seq_len = max_seq_len
        self.pad_token_id = pad_token_id

    def pack_sequences(self, sequences: List[List[int]]) -> List[Dict[str, torch.Tensor]]:
        """
        Packs multiple variable-length token lists into batches of exactly max_seq_len.
        Produces:
        - input_ids: tensor [max_seq_len]
        - position_ids: resets to 0 for each packed example!
        - attention_mask: 2D block-diagonal mask [max_seq_len, max_seq_len]
        """
        packed_batches = []
        curr_tokens: List[int] = []
        curr_positions: List[int] = []
        curr_boundaries: List[Tuple[int, int]] = []

        for seq in sequences:
            if len(seq) > self.max_seq_len:
                seq = seq[:self.max_seq_len]

            if len(curr_tokens) + len(seq) > self.max_seq_len:
                # Flush current packed batch
                packed_batches.append(self._finalize_batch(curr_tokens, curr_positions, curr_boundaries))
                curr_tokens = []
                curr_positions = []
                curr_boundaries = []

            start_idx = len(curr_tokens)
            end_idx = start_idx + len(seq)
            curr_tokens.extend(seq)
            curr_positions.extend(list(range(len(seq))))
            curr_boundaries.append((start_idx, end_idx))

        if curr_tokens:
            packed_batches.append(self._finalize_batch(curr_tokens, curr_positions, curr_boundaries))

        return packed_batches

    def _finalize_batch(self, tokens: List[int], positions: List[int], boundaries: List[Tuple[int, int]]) -> Dict[str, torch.Tensor]:
        actual_len = len(tokens)
        pad_len = self.max_seq_len - actual_len

        input_ids = tokens + [self.pad_token_id] * pad_len
        position_ids = positions + [0] * pad_len

        # Construct 2D attention mask: tokens can only attend to tokens in the SAME example
        mask = torch.zeros((self.max_seq_len, self.max_seq_len), dtype=torch.bool)
        for start, end in boundaries:
            mask[start:end, start:end] = True

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "position_ids": torch.tensor(position_ids, dtype=torch.long),
            "attention_mask": mask,
            "num_packed_samples": len(boundaries)
        }
