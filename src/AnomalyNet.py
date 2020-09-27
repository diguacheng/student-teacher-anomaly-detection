import torch
from torchsummary import summary
import torchvision.models as models
import torch.nn as nn


class AnomalyNet(nn.Module):
    '''Patch-based CNN for anomaly detection
       Designed to work with patches of size 65x65
    '''
    def __init__(self):
        super(AnomalyNet, self).__init__()
        self.path_size = 65
        self.conv1 = nn.Conv2d(3, 128, 5, 1)
        self.conv2 = nn.Conv2d(128, 128, 5, 1)
        self.conv3 = nn.Conv2d(128, 256, 5, 1)
        self.conv4 = nn.Conv2d(256, 256, 4, 1)
        self.conv5 = nn.Conv2d(256, 128, 1, 1)

        self.decode = nn.Linear(128, 512)

        self.max_pool = nn.MaxPool2d(2, 2)
        self.l_relu = nn.LeakyReLU(5e-3)

    def forward(self, x):
        x = self.l_relu(self.conv1(x))
        x = self.max_pool(x)
        x = self.l_relu(self.conv2(x))
        x = self.max_pool(x)
        x = self.l_relu(self.conv3(x))
        x = self.max_pool(x)
        x = self.l_relu(self.conv4(x))
        x = self.l_relu(self.conv5(x))
        x = self.l_relu(self.decode(torch.squeeze(x)))
        return x


if __name__ == '__main__':

    # Pretrained network for knowledge distillation
    resnet18 = models.resnet18(pretrained=True)
    resnet18 = nn.Sequential(*list(resnet18.children())[:-1])

    net = AnomalyNet()
    x = torch.rand((5, 3, 65, 65))

    y_net = net(x)
    y_resnet18 = resnet18(x)

    print(y_net.size())
    print(torch.squeeze(y_resnet18).size())

    net.cuda()
    summary(net, (3, 65, 65))
    