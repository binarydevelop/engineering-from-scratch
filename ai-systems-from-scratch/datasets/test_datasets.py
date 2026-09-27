import os
import sys
import pytest
import torch

sys.path.insert(0, os.path.dirname(__file__))

from dataset_cleaner import DatasetCleaner
from data_split_and_contamination import split_dataset, check_contamination
from instruction_formatter import ChatFormatter
from sequence_length_analyzer import SequenceLengthAnalyzer
from sample_packer import SamplePacker

def test_dataset_cleaner():
    cleaner = DatasetCleaner()
    raw = [
        {"instruction": "What is 2+2?", "output": "4"},
        {"instruction": "  what is 2+2? ", "output": "4"}, # Duplicate
        {"instruction": "What is 2+2?", "output": "5"},     # Contradiction!
        {"instruction": "", "output": "Empty input"},       # Malformed
        {"instruction": "Valid query", "output": "Valid answer"}
    ]
    cleaned = cleaner.clean_dataset(raw)
    assert len(cleaned) == 2
    assert cleaner.duplicates_removed == 1
    assert cleaner.contradictions_removed == 1
    assert cleaner.malformed_removed == 1

def test_split_and_contamination():
    data = [{"instruction": f"Query {i}", "input": "", "output": f"Answer {i}"} for i in range(100)]
    train, val, test = split_dataset(data, 0.8, 0.1, 0.1, seed=42)
    assert len(train) == 80
    assert len(val) == 10
    assert len(test) == 10

    # Inject deliberate contamination
    contaminated_eval = [{"instruction": "Query 5", "input": ""}]
    leaks = check_contamination(train, contaminated_eval, ngram_size=2, threshold=0.8)
    assert len(leaks) == 1

def test_chat_formatter():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
    chatml = ChatFormatter.format_chatml(messages)
    assert "<|im_start|>system" in chatml
    assert "<|im_start|>user" in chatml
    assert "<|im_start|>assistant\n" in chatml

    llama3 = ChatFormatter.format_llama3(messages)
    assert "<|start_header_id|>system<|end_header_id|>" in llama3
    assert "<|start_header_id|>user<|end_header_id|>" in llama3

def test_sequence_length_analyzer():
    analyzer = SequenceLengthAnalyzer()
    lengths = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    stats = analyzer.analyze_token_lengths(lengths)
    assert stats["count"] == 10
    assert stats["median_p50"] == 55.0
    trunc = analyzer.compute_truncation_loss(lengths, target_cutoff=50)
    assert trunc["truncated_samples"] == 5

def test_sample_packer():
    packer = SamplePacker(max_seq_len=16)
    seqs = [[1, 2, 3], [4, 5, 6, 7], [8, 9, 10]]
    batches = packer.pack_sequences(seqs)
    assert len(batches) == 1
    batch = batches[0]
    assert batch["num_packed_samples"] == 3
    # Verify attention mask doesn't leak: token 0 (in seq 1) cannot attend to token 4 (in seq 2)
    assert batch["attention_mask"][0, 4].item() is False
    # But token 0 can attend to token 2 (same seq)
    assert batch["attention_mask"][0, 2].item() is True
