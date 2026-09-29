# Malicious URL Detection using Multi-Representation CNN

A CNN-based malicious URL detection system that combines character-level URL representations with handcrafted lexical and structural URL features to classify URLs as Safe or Malicious.

## Overview

Malicious URLs can contain structural and lexical patterns that differ from legitimate URLs. This project uses deep learning to analyse these patterns and classify URLs into two categories:

- Safe
- Malicious

The system uses two complementary representations of the same URL:

- Character-level URL sequence
- Engineered lexical and structural URL features

These representations are processed by a multi-input CNN and combined through feature fusion before producing the final prediction.

## Key Features

- Character-level URL tokenisation
- Fixed-length URL sequence representation
- 59 engineered URL features
- CNN-based representation learning
- Feature fusion
- Binary Safe/Malicious classification
- Malicious probability output
- FastAPI backend
- Browser-based frontend
- Real-time URL analysis

## Model

The model accepts two inputs:

1. A tokenised URL sequence padded to a length of 100.
2. A 59-dimensional engineered URL feature vector.

The character-level representation is processed through the CNN branch, while the engineered features provide additional lexical and structural information. The learned representations are combined before the final classification layer.

The deployed model is:

```text
models/malicious_cnn_model_v2.keras
