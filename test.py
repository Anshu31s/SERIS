import torch

# Check PyTorch version
print("PyTorch version:", torch.__version__)

# Check if CUDA is available
cuda_available = torch.cuda.is_available()
print("CUDA Available:", cuda_available)

# If CUDA is available, show GPU name and count
if cuda_available:
    print("Number of GPUs:", torch.cuda.device_count())
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("Current CUDA Device:", torch.cuda.current_device())
