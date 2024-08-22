import faiss
import numpy as np

class ImageFeatureStore:
    def __init__(self, dim=512):
        """
        初始化图像特征存储器。

        参数:
        dim (int): 图像特征向量的维度。
        """
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # 使用内积（dot product）作为度量标准

    def add(self, vectors):
        """
        添加图像特征向量到索引中。

        参数:
        vectors (np.array): 要添加的特征向量，形状为 (n_samples, dim)。
        """
        self.index.add(vectors)

    def search(self, query_vectors, k=5):
        """
        搜索与查询向量最相似的图像特征向量。

        参数:
        query_vectors (np.array): 查询的特征向量，形状为 (n_queries, dim)。
        k (int): 返回最相似的top k个结果。

        返回:
        (distances, indices): 与查询向量最相似的k个特征向量的距离和索引。
        """
        distances, indices = self.index.search(query_vectors, k)
        return distances, indices

    def count(self):
        """
        返回索引中的特征向量数量。

        返回:
        int: 索引中存储的特征向量数量。
        """
        return self.index.ntotal

    def save_to_file(self, file_path):
        """
        将索引和特征向量保存到文件。

        参数:
        file_path (str): 要保存的文件路径。
        """
        faiss.write_index(self.index, file_path)
        print(f"索引已保存到 {file_path}")

    def load_from_file(self, file_path):
        """
        从文件加载索引和特征向量。

        参数:
        file_path (str): 要加载的文件路径。
        """
        self.index = faiss.read_index(file_path)
        print(f"索引已从 {file_path} 加载")

    def clear_index(self):
    """
    清空当前的索引。
    """
    self.index = faiss.IndexFlatIP(self.dim)  # 重新初始化索引
    print("索引已清空")

# test 
if __name__ == "__main__":
    # 假设每个图像特征向量的维度为128
    feature_store = ImageFeatureStore(dim=128)
    
    # 创建一些随机特征向量（10个样本，每个128维）
    vectors = np.random.random((10, 128)).astype('float32')
    
    # 添加向量到索引
    feature_store.add(vectors)
    
    # 创建一个查询向量（1个样本，128维）
    query_vector = np.random.random((1, 128)).astype('float32')
    
    # 搜索最相似的5个向量
    distances, indices = feature_store.search(query_vector, k=5)
    
    print("最相似的向量距离:", distances)
    print("最相似的向量索引:", indices)
    print("索引中的总向量数量:", feature_store.count())