import torch
# check if cuda is available
print(torch.cuda.is_available())
# display the graphic card that pytorch is using
print(torch.cuda.get_device_name(torch.cuda.current_device()))