import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Your project description")

    # 添加命令行参数
    # parser.add_argument('--input', type=str, required=True, help="Input file path")
    # parser.add_argument('--output', type=str, required=True, help="Output file path")
    # parser.add_argument('--verbose', action='store_true', help="Increase output verbosity")
    
    parser.add_argument('--clip_model', type=str, help="clip model type", default="openai/clip-vit-base-patch32")
    parser.add_argument('--embed_dim', type=int, help="feature dim", default=512)
    
    # 解析参数
    args = parser.parse_args()
    return args
