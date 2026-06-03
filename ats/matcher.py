"""Core matching logic: combines semantic similarity with skill gap analysis."""
from typing import Dict, List
 
import numpy as np
 
from embedder import TfIdfWord2VecEmbedder
from skill_extractor import SkillExtractor