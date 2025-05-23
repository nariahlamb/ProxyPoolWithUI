# GitHub Actions 自动构建说明

本项目已配置GitHub Actions，可以自动构建Docker镜像并推送到DockerHub。

## 配置步骤

1. 在GitHub仓库页面，点击 **Settings** 选项卡
2. 在左侧菜单中，选择 **Secrets and variables** > **Actions**
3. 点击 **New repository secret** 创建以下两个密钥：

   - `DOCKERHUB_USERNAME`: 您的DockerHub用户名
   - `DOCKERHUB_TOKEN`: 您的DockerHub访问令牌（不是密码）

## 获取DockerHub访问令牌

为了安全起见，建议使用访问令牌而不是DockerHub密码：

1. 登录DockerHub
2. 点击右上角您的头像，选择 **Account Settings**
3. 在左侧菜单中，选择 **Security**
4. 点击 **New Access Token**
5. 输入令牌名称（如"GitHub Actions"）并选择适当的权限（至少需要"Read & Write"权限）
6. 复制生成的令牌，将其添加到GitHub Secrets中

## 触发构建

配置完成后，以下操作会触发自动构建：

- 向`main`分支推送代码
- 创建以`v`开头的标签（例如`v1.0.0`）
- 创建针对`main`分支的Pull Request（但不会推送到DockerHub）

## 镜像标签规则

构建的Docker镜像将使用以下命名规则：

- 分支构建：`username/proxy-pool:main`
- 标签构建：`username/proxy-pool:1.0.0`和`username/proxy-pool:1.0`
- 主分支构建：`username/proxy-pool:latest`和基于提交SHA的标签

## 多架构支持

本项目的自动构建流程支持同时构建多种CPU架构的Docker镜像，包括：

- `linux/amd64`（x86_64 架构，适用于大多数服务器和PC）
- `linux/arm64`（ARM64 架构，适用于树莓派4、AWS Graviton、Apple Silicon等ARM设备）

这意味着无论您使用的是x86服务器还是ARM设备，都可以直接使用我们的Docker镜像，Docker会自动拉取与您设备匹配的镜像。

使用以下命令可以查看镜像支持的架构：

```bash
docker manifest inspect USERNAME/proxy-pool:latest
```

## 测试构建流程

配置完成后，您可以通过以下方式测试自动构建：

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0
```

然后在GitHub仓库的Actions选项卡中查看构建进度。 