import torch
import torch.nn.functional as F

# Fake embeddings for 3 tokens
X = torch.randn(3, 4)

Wq = torch.randn(4, 4)
Wk = torch.randn(4, 4)
Wv = torch.randn(4, 4)

Q = X @ Wq
K = X @ Wk
V = X @ Wv

scores = Q @ K.T
scaled = scores / (4 ** 0.5)

weights = F.softmax(scaled, dim=1)

output = weights @ V

print(output)
