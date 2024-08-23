# 制作Database
from tot_args import parse_args
from agrirag import ImageFeatureStore
from agrirag import CLIPFeatureExtractor
# from agrirag.database.faiss_db import ImageFeatureStore
# from agrirag.clip.features import CLIPFeatureExtractor

args = parse_args()


DB = ImageFeatureStore(args.embed_dim)
CLIP_model = CLIPFeatureExtractor(args.clip_model)

